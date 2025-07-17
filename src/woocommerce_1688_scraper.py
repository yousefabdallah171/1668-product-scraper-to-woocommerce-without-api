#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1688.com Product Scraper for WooCommerce
Extracts product data from 1688.com, translates to English, and formats for WooCommerce import
"""
import time
import os
import json
import csv
import cloudscraper
from bs4 import BeautifulSoup
import re
from datetime import datetime
import logging
import sys
import translators as ts
import requests
from PIL import Image
from io import BytesIO
import uuid
import shutil
from urllib.parse import urljoin, urlparse
import hashlib

# Always use root-level output and logs directories
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(ROOT_DIR, '..'))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')

# Configure logging
os.makedirs(LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, 'woocommerce_scraper.log'), encoding='utf-8')
    ]
)

# Add console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
logging.getLogger().addHandler(console_handler)

def log(message, level="INFO"):
    """Log a message with timestamp and level"""
    try:
        if level == "INFO":
            logging.info(message)
        elif level == "ERROR":
            logging.error(message)
        elif level == "WARNING":
            logging.warning(message)
        elif level == "DEBUG":
            logging.debug(message)
    except UnicodeEncodeError:
        # Handle encoding errors for console output
        try:
            ascii_message = message.encode('ascii', 'replace').decode('ascii')
            print(f"[{level}] {ascii_message} (contains non-ASCII characters)")
        except:
            print(f"[{level}] <Message contains characters that cannot be displayed>")

def fix_image_url(url):
    """Clean and fix image URL and filter out low-quality images"""
    if not url or not isinstance(url, str):
        return None
    
    # Clean up the URL
    url = url.strip()
    
    # Skip low-quality images
    if any(q in url.lower() for q in ['search', 'summ', '_50x50', '_100x100', '_200x200', 
                                    '_300x300', '_400x400', '_500x500', '_600x600',
                                    'q60', 'q50', 'q40', 'q30']):
        return None
    
    # Handle malformed JSON URLs first
    if url.startswith('{"') and '"http' in url:
        try:
            data = json.loads(url)
            # Try common image URL fields in JSON
            for field in ['url', 'image', 'imageUrl', 'imageURL', 'imgUrl', 'img', 'fullPathImageURI']:
                if field in data and isinstance(data[field], str) and 'http' in data[field]:
                    url = data[field]
                    break
        except (json.JSONDecodeError, TypeError):
            # If not valid JSON, try to extract URL with regex
            url_match = re.search(r'https?://[^\s\"\']+', url)
            if url_match:
                url = url_match.group(0)
    
    # Remove any trailing query parameters that might cause issues
    url = url.split('?')[0]
    
    # Handle URLs that might be in a JSON-like format
    if 'ImageURI:' in url:
        url = url.split('ImageURI:')[-1].strip('"\'')
    
    # Handle URLs that might have size prefixes
    if 'ImageURI:http' in url:
        url = 'http' + url.split('http', 1)[1]
    
    # Remove any trailing commas or other invalid characters
    url = url.rstrip(',;')
    
    # Remove any trailing slashes
    url = url.rstrip('/')
    
    # Make sure the URL starts with http
    if not url.startswith(('http://', 'https://')):
        return None
    
    # Remove any size parameters from the URL
    if '_.webp' in url:
        url = url.split('_.webp')[0] + '.jpg'
    
    # Remove any size parameters from the URL (common in 1688 URLs)
    if '_.jpg' in url:
        url = url.split('_.jpg')[0] + '.jpg'
    elif '_.jpeg' in url:
        url = url.split('_.jpeg')[0] + '.jpeg'
    elif '_.png' in url:
        url = url.split('_.png')[0] + '.png'
    
    # Remove any other size parameters that might be in the URL
    for size_param in ['_50x50', '_100x100', '_200x200', '_300x300', '_400x400', 
                      '_500x500', '_600x600', '_800x800', '_1000x1000', '_1200x1200',
                      '_1500x1500', '_2000x2000', '.220x220', '.310x310']:
        if size_param in url:
            url = url.replace(size_param, '')
    
    # Remove any quality parameters
    if 'Q90' in url and '.jpg' in url:
        url = url.split('Q90')[0] + '.jpg'
    
    # Remove any other quality parameters
    for q_param in ['Q75', 'Q60', 'Q50', 'Q40', 'Q30']:
        if q_param in url and '.jpg' in url:
            url = url.split(q_param)[0] + '.jpg'
    
    # Remove any other query parameters that might be in the URL
    if '?' in url:
        base_url = url.split('?')[0]
        # Only keep the base URL if it ends with an image extension
        if any(base_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            url = base_url
    
    # Final cleanup of any remaining size indicators
    url = re.sub(r'[_-]\d{2,4}x\d{2,4}', '', url)
    
    # Remove any trailing dots or invalid characters
    url = url.rstrip('.').strip()
    
    return url if any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']) else None

def extract_images_from_1688(html_content, soup):
    """Extract images using 1688's actual data structure"""
    images = []
    
    # Method 1: Extract from JSON data in script tags
    script_tags = soup.find_all('script')
    for script in script_tags:
        if script.string and ('imageList' in script.string or 'images' in script.string):
            try:
                # Look for image arrays in JavaScript
                image_patterns = [
                    r'"imageList":\s*\[(.*?)\]',
                    r'"images":\s*\[(.*?)\]',
                    r'"imgUrl":"([^"]+)"',
                    r'"fullPathImageURI":"([^"]+)"'
                ]
                
                for pattern in image_patterns:
                    matches = re.findall(pattern, script.string)
                    for match in matches:
                        if isinstance(match, str) and 'http' in match:
                            clean_url = fix_image_url(match)
                            if clean_url and clean_url not in images:
                                images.append(clean_url)
                                
            except Exception as e:
                continue
    
    # Method 2: Look for current 1688 image selectors
    img_selectors = [
        'img[data-lazy-src]',  # Lazy loaded images
        'img[data-original]',   # Original images
        '.image-view img',      # Image viewer
        '.offer-img img',       # Offer images
        '[class*="image"] img', # Any image container
    ]
    
    for selector in img_selectors:
        imgs = soup.select(selector)
        for img in imgs:
            # Try multiple attributes
            for attr in ['data-lazy-src', 'data-original', 'data-src', 'src']:
                img_url = img.get(attr)
                if img_url:
                    clean_url = fix_image_url(img_url)
                    if clean_url and clean_url not in images:
                        images.append(clean_url)
                    break
    
    # Method 3: Regex for 1688 CDN URLs in HTML
    cdn_pattern = r'(https://cbu01\.alicdn\.com/[^"\s>]+\.(?:jpg|jpeg|png|webp))'
    cdn_matches = re.findall(cdn_pattern, html_content)
    for match in cdn_matches:
        clean_url = fix_image_url(match)
        if clean_url and clean_url not in images:
            images.append(clean_url)
    
    # If no images were successfully extracted, use online sample images
    if not images:
        log("No product images could be found, using online sample images")
        
        # Use a reliable placeholder image
        images = ["https://via.placeholder.com/800x800?text=No+Image+Available"]
        log("Using placeholder image")
            
        log(f"Added {len(images)} online sample images")
    
    return images

def extract_images_from_1688_json(html_content):
    """Extract images from 1688's JSON data structures - the most reliable method"""
    images = []
    
    try:
        # Method 1: Extract from offerImgList in gallery section
        offer_img_pattern = r'"offerImgList":\[(.*?)\]'
        offer_matches = re.findall(offer_img_pattern, html_content, re.DOTALL)
        
        for match in offer_matches:
            # Clean the match and extract URLs
            urls = re.findall(r'"([^"]*cbu01\.alicdn\.com[^"]*\.jpg)"', match)
            for url in urls:
                clean_url = fix_image_url(url)
                if clean_url and clean_url not in images:
                    images.append(clean_url)
                    log(f"Found image from offerImgList: {clean_url}")
        
        # Method 2: Extract from mainImageList in offerDetail section
        main_img_pattern = r'"mainImageList":\[(.*?)\]'
        main_matches = re.findall(main_img_pattern, html_content, re.DOTALL)
        
        for match in main_matches:
            # Look for fullPathImageURI in each image object
            full_path_matches = re.findall(r'"fullPathImageURI":"([^"]*)"', match)
            for url in full_path_matches:
                clean_url = fix_image_url(url)
                if clean_url and clean_url not in images:
                    images.append(clean_url)
                    log(f"Found image from mainImageList: {clean_url}")
        
        # Method 3: Extract from imageList in offerDetail section
        img_list_pattern = r'"imageList":\[(.*?)\]'
        img_list_matches = re.findall(img_list_pattern, html_content, re.DOTALL)
        
        for match in img_list_matches:
            # Look for fullPathImageURI in each image object
            full_path_matches = re.findall(r'"fullPathImageURI":"([^"]*)"', match)
            for url in full_path_matches:
                clean_url = fix_image_url(url)
                if clean_url and clean_url not in images:
                    images.append(clean_url)
                    log(f"Found image from imageList: {clean_url}")
        
        # Method 4: Direct regex for 1688 CDN URLs
        cdn_pattern = r'https://cbu01\.alicdn\.com/img/ibank/[^"\s>]+\.jpg'
        cdn_matches = re.findall(cdn_pattern, html_content)
        for url in cdn_matches:
            clean_url = fix_image_url(url)
            if clean_url and clean_url not in images:
                images.append(clean_url)
                log(f"Found image from CDN pattern: {clean_url}")
        
        log(f"Total images extracted from JSON: {len(images)}")
        return images
        
    except Exception as e:
        log(f"Error extracting images from JSON: {str(e)}", "ERROR")
        return []

def debug_extract_images_from_1688(html_content, soup, url):
    """Enhanced debug version to extract images with multiple methods"""
    images = []
    base_url = '/'.join(url.split('/')[:3])
    
    log(f"Starting image extraction for URL: {url}", "DEBUG")
    
    # Method 1: Direct image URLs in HTML
    log("Method 1: Looking for direct image URLs in HTML...", "DEBUG")
    img_tags = soup.find_all('img', src=True)
    log(f"Found {len(img_tags)} <img> tags", "DEBUG")
    
    for img in img_tags:
        src = img.get('src', '').strip()
        data_src = img.get('data-src', '').strip()
        data_original = img.get('data-original', '').strip()
        
        # Check all possible image sources
        for img_src in [src, data_src, data_original]:
            if not img_src:
                continue
                
            # Handle protocol-relative URLs
            if img_src.startswith('//'):
                img_src = 'https:' + img_src
            # Handle relative URLs
            elif not img_src.startswith('http'):
                img_src = urljoin(base_url, img_src)
            
            # Clean up the URL
            img_src = fix_image_url(img_src)
            
            # Check if it's a valid image URL
            if (img_src and 
                'http' in img_src and 
                any(x in img_src for x in ['.jpg', '.jpeg', '.png', '.webp']) and
                not any(x in img_src.lower() for x in ['logo', 'icon', 'placeholder', 'spacer', 'pixel']) and
                img_src not in images):
                
                images.append(img_src)
                log(f"  Added image: {img_src}", "DEBUG")
    
    # Method 2: Look in JSON data
    log("\nMethod 2: Looking for images in JSON data...", "DEBUG")
    json_patterns = [
        r'window\.runParams\s*=\s*({.+?});',
        r'window\.detailData\s*=\s*({.+?});',
        r'"imageList"\s*:\s*(\[.*?\])',
        r'"imageUrls"\s*:\s*(\[.*?\])',
        r'"picList"\s*:\s*(\[.*?\])',
        r'"imageUrl"\s*:\s*\"([^\"]+)\"',
        r'"picUrl"\s*:\s*\"([^\"]+)\"',
        r'"image_url"\s*:\s*\"([^\"]+)\"',
        r'"img"\s*:\s*\"([^\"]+)\"',
        r'"url"\s*:\s*\"([^\"]+)\"'
    ]
    
    for pattern in json_patterns:
        try:
            matches = re.finditer(pattern, html_content, re.DOTALL)
            for match in matches:
                if not match.group(1):
                    continue
                    
                # Handle JSON arrays
                if match.group(1).startswith('['):
                    try:
                        urls = json.loads(match.group(1))
                        if isinstance(urls, list):
                            for url in urls:
                                if isinstance(url, str) and 'http' in url:
                                    fixed_url = fix_image_url(url)
                                    if fixed_url and fixed_url not in images:
                                        images.append(fixed_url)
                                        log(f"  Added image from JSON array: {fixed_url}", "DEBUG")
                    except json.JSONDecodeError:
                        pass
                # Handle single URL
                elif 'http' in match.group(1):
                    fixed_url = fix_image_url(match.group(1))
                    if (fixed_url and 
                        fixed_url not in images and 
                        any(x in fixed_url for x in ['.jpg', '.jpeg', '.png', '.webp'])):
                        images.append(fixed_url)
                        log(f"  Added image from JSON: {fixed_url}", "DEBUG")
        except Exception as e:
            log(f"Error processing pattern {pattern}: {str(e)}", "DEBUG")
    
    # Method 3: Look in meta tags
    log("\nMethod 3: Looking for images in meta tags...", "DEBUG")
    for meta in soup.find_all('meta', property=re.compile(r'og:image')):
        if meta.get('content'):
            img_url = meta['content']
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            if img_url not in images:
                images.append(img_url)
                log(f"  Added image from meta tag: {img_url}", "DEBUG")
    
    # Clean up and validate URLs
    cleaned_images = []
    for img in images:
        try:
            # Remove query parameters that might cause issues
            img = img.split('?')[0]
            # Ensure URL is absolute
            if not img.startswith('http'):
                img = urljoin(base_url, img)
            # Basic validation
            if (any(x in img for x in ['.jpg', '.jpeg', '.png', '.webp']) and 
                not any(x in img.lower() for x in ['logo', 'icon', 'placeholder', 'spacer']) and
                img not in cleaned_images):
                cleaned_images.append(img)
        except Exception as e:
            log(f"Error cleaning image URL {img}: {str(e)}", "DEBUG")
    
    log(f"\nTotal images found: {len(cleaned_images)}", "DEBUG")
    return cleaned_images[:20]  # Return max 20 images

def extract_description_from_feature_attributes(html_content):
    """Extract product description and create structured HTML tables from 1688 JSON data"""
    try:
        html_parts = []
        
        # Extract product details from offerDetail
        offer_detail_pattern = r'\"offerDetail\":\s*\{([^}]+)\}'
        offer_detail_matches = re.findall(offer_detail_pattern, html_content, re.DOTALL)
        
        if offer_detail_matches:
            log(f"Found {len(offer_detail_matches)} offerDetail sections")
            
            for i, match in enumerate(offer_detail_matches):
                # Extract title, seller, company, promotion, services
                title_match = re.search(r'\"title\":\s*\"([^\"]+)\"', match)
                seller_match = re.search(r'\"seller\":\s*\"([^\"]+)\"', match)
                company_match = re.search(r'\"company\":\s*\"([^\"]+)\"', match)
                promotion_match = re.search(r'\"promotion\":\s*\"([^\"]+)\"', match)
                services_match = re.search(r'\"services\":\s*\"([^\"]+)\"', match)
                
                if title_match or seller_match or company_match or promotion_match or services_match:
                    html_parts.append('<h3>商品详情 (Product Details)</h3>')
                    html_parts.append('<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">')
                    html_parts.append('<tr><th style="background-color: #f5f5f5; padding: 8px;">项目 (Item)</th><th style="background-color: #f5f5f5; padding: 8px;">详情 (Details)</th></tr>')
                    
                    if title_match:
                        html_parts.append(f'<tr><td style="padding: 8px;"><strong>产品标题 (Title)</strong></td><td style="padding: 8px;">{title_match.group(1)}</td></tr>')
                    if seller_match:
                        html_parts.append(f'<tr><td style="padding: 8px;"><strong>卖家 (Seller)</strong></td><td style="padding: 8px;">{seller_match.group(1)}</td></tr>')
                    if company_match:
                        html_parts.append(f'<tr><td style="padding: 8px;"><strong>公司 (Company)</strong></td><td style="padding: 8px;">{company_match.group(1)}</td></tr>')
                    if promotion_match:
                        html_parts.append(f'<tr><td style="padding: 8px;"><strong>促销信息 (Promotion)</strong></td><td style="padding: 8px;">{promotion_match.group(1)}</td></tr>')
                    if services_match:
                        html_parts.append(f'<tr><td style="padding: 8px;"><strong>服务 (Services)</strong></td><td style="padding: 8px;">{services_match.group(1)}</td></tr>')
                    
                    html_parts.append('</table>')
        
        # Extract product attributes from featureAttributes - Improved parsing
        feature_pattern = r'\"featureAttributes\":\s*\[(.*?)\]'
        feature_matches = re.findall(feature_pattern, html_content, re.DOTALL)
        
        if feature_matches:
            log(f"Found {len(feature_matches)} featureAttributes sections")
            
            for i, match in enumerate(feature_matches):
                log(f"Processing featureAttributes section {i+1}, length: {len(match)}")
                
                # Extract individual attribute objects with better pattern
                # Look for complete attribute objects with nested structure
                attr_objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', match)
                attributes = []
                
                log(f"Found {len(attr_objects)} attribute objects")
                
                for j, attr_obj in enumerate(attr_objects):
                    # Extract name and value from each attribute object
                    name_match = re.search(r'\"name\":\s*\"([^\"]+)\"', attr_obj)
                    value_match = re.search(r'\"value\":\s*\"([^\"]+)\"', attr_obj)
                    
                    if name_match and value_match:
                        name = name_match.group(1)
                        value = value_match.group(1)
                        if name and value and len(value.strip()) > 0:
                            attributes.append((name, value))
                            log(f"Attribute {j+1}: {name} = {value}")
                
                if attributes:
                    html_parts.append('<h3>商品属性 (Product Attributes)</h3>')
                    html_parts.append('<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">')
                    html_parts.append('<tr><th style="background-color: #f5f5f5; padding: 8px;">属性 (Attribute)</th><th style="background-color: #f5f5f5; padding: 8px;">值 (Value)</th></tr>')
                    
                    for attr_name, attr_value in attributes:
                        html_parts.append(f'<tr><td style="padding: 8px;"><strong>{attr_name}</strong></td><td style="padding: 8px;">{attr_value}</td></tr>')
                    
                    html_parts.append('</table>')
                    log(f"Extracted {len(attributes)} product attributes")
                else:
                    log("No attributes found in featureAttributes section")
        
        # Extract packaging information from productPackInfo - Improved parsing
        pack_pattern = r'\"productPackInfo\":\s*\{([^}]+)\}'
        pack_matches = re.findall(pack_pattern, html_content, re.DOTALL)
        
        if pack_matches:
            log(f"Found {len(pack_matches)} productPackInfo sections")
            
            for i, match in enumerate(pack_matches):
                # Extract packaging details with better pattern matching
                pack_attributes = []
                
                # Look for specific packaging fields
                unit_weight_match = re.search(r'\"unitWeight\":\s*([0-9.]+)', match)
                if unit_weight_match:
                    pack_attributes.append(("商品件重尺", f"{unit_weight_match.group(1)} kg"))
                
                # Look for other packaging fields
                pack_fields = [
                    ('uiType', '包装类型'),
                    ('label', '包装标签'),
                    ('sku', 'SKU信息'),
                    ('sku1', 'SKU详情1'),
                    ('sku2', 'SKU详情2')
                ]
                
                for field, label in pack_fields:
                    field_match = re.search(f'\"{field}\":\s*\"([^\"]+)\"', match)
                    if field_match:
                        pack_attributes.append((label, field_match.group(1)))
                
                if pack_attributes:
                    html_parts.append('<h3>包装信息 (Packaging Information)</h3>')
                    html_parts.append('<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">')
                    html_parts.append('<tr><th style="background-color: #f5f5f5; padding: 8px;">包装项目 (Packaging Item)</th><th style="background-color: #f5f5f5; padding: 8px;">规格 (Specification)</th></tr>')
                    
                    for pack_name, pack_value in pack_attributes:
                        html_parts.append(f'<tr><td style="padding: 8px;"><strong>{pack_name}</strong></td><td style="padding: 8px;">{pack_value}</td></tr>')
                    
                    html_parts.append('</table>')
                    log(f"Extracted {len(pack_attributes)} packaging attributes")
        
        # Extract additional product information from other JSON structures
        additional_patterns = [
            (r'\"productInfo\":\s*\{([^}]+)\}', '产品信息 (Product Information)'),
            (r'\"specification\":\s*\{([^}]+)\}', '规格参数 (Specifications)'),
            (r'\"material\":\s*\"([^\"]+)\"', '材质 (Material)'),
            (r'\"brand\":\s*\"([^\"]+)\"', '品牌 (Brand)'),
            (r'\"model\":\s*\"([^\"]+)\"', '型号 (Model)'),
            (r'\"color\":\s*\"([^\"]+)\"', '颜色 (Color)'),
            (r'\"size\":\s*\"([^\"]+)\"', '尺寸 (Size)'),
            (r'\"weight\":\s*\"([^\"]+)\"', '重量 (Weight)'),
            (r'\"origin\":\s*\"([^\"]+)\"', '产地 (Origin)'),
            (r'\"warranty\":\s*\"([^\"]+)\"', '保修 (Warranty)'),
            (r'\"subject\":\s*\"([^\"]+)\"', '产品标题 (Product Title)'),
            (r'\"companyName\":\s*\"([^\"]+)\"', '公司名称 (Company Name)'),
            (r'\"sellerLoginId\":\s*\"([^\"]+)\"', '卖家 (Seller)'),
            (r'\"leafCategoryName\":\s*\"([^\"]+)\"', '产品类别 (Category)'),
            (r'\"saleCount\":\s*([0-9]+)', '销量 (Sales Count)'),
            (r'\"unit\":\s*\"([^\"]+)\"', '单位 (Unit)')
        ]
        
        additional_info = []
        for pattern, label in additional_patterns:
            matches = re.findall(pattern, html_content, re.DOTALL)
            for match in matches:
                if match and len(match.strip()) > 0:
                    additional_info.append((label, match))
        
        if additional_info:
            html_parts.append('<h3>其他信息 (Additional Information)</h3>')
            html_parts.append('<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">')
            html_parts.append('<tr><th style="background-color: #f5f5f5; padding: 8px;">信息类型 (Info Type)</th><th style="background-color: #f5f5f5; padding: 8px;">详情 (Details)</th></tr>')
            
            for info_type, info_value in additional_info:
                html_parts.append(f'<tr><td style="padding: 8px;"><strong>{info_type}</strong></td><td style="padding: 8px;">{info_value}</td></tr>')
            
            html_parts.append('</table>')
        
        # Combine all parts
        if html_parts:
            full_description = '\n'.join(html_parts)
            log(f"Created structured description with {len(html_parts)} sections")
            return full_description
        else:
            log("No structured data found for description")
            return ""
            
    except Exception as e:
        log(f"Error extracting structured description: {str(e)}")
        return ""

def extract_description_from_detail_url(html_content):
    """Extract product description from detailUrl HTML content with enhanced parsing"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        description_parts = []
        
        # Method 1: Try to extract from JSON data in detailUrl content
        json_patterns = [
            r'"description":"([^"]+)"',
            r'"content":"([^"]+)"',
            r'"text":"([^"]+)"',
            r'"detail":"([^"]+)"'
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html_content)
            for match in matches:
                if len(match) > 20:  # Minimum meaningful content
                    description_parts.append(match)
                    log(f"Found description in JSON: {len(match)} characters")
        
        # Method 2: Try multiple selectors for description content
        desc_selectors = [
            '.detail-content',
            '.product-description',
            '.description-content',
            '.detail-desc',
            '#description',
            '.html-description',
            'div[class*="desc"]',
            'div[class*="detail"]',
            '.content',
            '.text',
            'p',
            'div'
        ]
        
        for selector in desc_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Get text content
                text_content = element.get_text(strip=True)
                if len(text_content) > 50:  # Minimum meaningful content
                    # Clean up the text
                    text_content = re.sub(r'\s+', ' ', text_content)  # Remove extra whitespace
                    text_content = text_content.strip()
                    
                    if text_content and text_content not in description_parts:
                        description_parts.append(text_content)
                        log(f"Found description using selector '{selector}': {len(text_content)} characters")
        
        # Method 3: Extract from HTML attributes that might contain descriptions
        for tag in soup.find_all(['div', 'p', 'span', 'section']):
            # Check data attributes
            for attr in ['data-content', 'data-description', 'data-text', 'data-detail']:
                if tag.has_attr(attr):
                    content = tag[attr]
                    if len(content) > 20:
                        description_parts.append(content)
                        log(f"Found description in data attribute '{attr}': {len(content)} characters")
        
        # Method 4: Extract from title and meta tags
        title_tag = soup.find('title')
        if title_tag and title_tag.text:
            title_text = title_tag.text.strip()
            if len(title_text) > 10:
                description_parts.append(f"Title: {title_text}")
                log(f"Added title: {title_text}")
        
        # Check meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_content = meta_desc['content'].strip()
            if len(desc_content) > 20:
                description_parts.append(desc_content)
                log(f"Added meta description: {len(desc_content)} characters")
        
        # Method 5: Fallback: extract all meaningful text from body
        if not description_parts:
            body_text = soup.get_text(strip=True)
            if len(body_text) > 100:
                # Clean up the text
                body_text = re.sub(r'\s+', ' ', body_text)
                body_text = body_text.strip()
                
                # Take first 2000 characters
                body_text = body_text[:2000]
                description_parts.append(body_text)
                log(f"Using fallback: extracted all text from body: {len(body_text)} characters")
        
        if description_parts:
            # Remove duplicates while preserving order
            unique_parts = []
            for part in description_parts:
                if part not in unique_parts:
                    unique_parts.append(part)
            
            # Join with separator
            result = " | ".join(unique_parts)
            log(f"Successfully extracted description from detailUrl with {len(unique_parts)} parts")
            return result
        else:
            log("No description content found in detailUrl", "WARNING")
            return None
        
    except Exception as e:
        log(f"Error extracting description from detailUrl: {str(e)}", "ERROR")
        return None

class WooCommerceProduct:
    """Class to handle product data structure and WooCommerce formatting"""
    def __init__(self):
        self.data = {
            'Type': 'simple',
            'SKU': '',
            'Name': '',
            'Published': '1',
            'Featured': '0',
            'Visibility in catalog': 'visible',
            'Short description': '',
            'Description': '',
            'Date sale price starts': '',
            'Date sale price ends': '',
            'Tax status': 'taxable',
            'Tax class': '',
            'In stock?': 'yes',
            'Stock': '',
            'Backorders allowed?': '0',
            'Sold individually?': '0',
            'Weight (kg)': '',
            'Length (cm)': '',
            'Width (cm)': '',
            'Height (cm)': '',
            'Allow customer reviews?': '1',
            'Purchase note': '',
            'Sale price': '',
            'Regular price': '',
            'Categories': '',
            'Tags': '',
            'Shipping class': '',
            'Images': '',
            'Download limit': '',
            'Download expiry days': '',
            'Parent': '',
            'Grouped products': '',
            'Upsells': '',
            'Cross-sells': '',
            'External URL': '',
            'Button text': '',
            'Position': '',
            'Attribute 1 name': '',
            'Attribute 1 value(s)': '',
            'Attribute 1 visible': '1',
            'Attribute 1 global': '1',
            'Attribute 2 name': '',
            'Attribute 2 value(s)': '',
            'Attribute 2 visible': '1',
            'Attribute 2 global': '1',
            'Product Link': ''
        }
        self.images = []
        self.source_url = ''

    def set_basic_info(self, name, description, price, sku, url, short_description=None):
        """Set basic product information"""
        self.data['Name'] = name
        self.data['Description'] = description
        self.data['Regular price'] = price.replace('¥', '')  # Remove currency symbol
        self.data['SKU'] = sku
        self.data['Short description'] = short_description if short_description else self.generate_short_description(description)
        self.source_url = url
        self.data['Product Link'] = url

    def add_image(self, image_path):
        """Add an image path to the product"""
        if image_path and image_path not in self.images:
            self.images.append(image_path)
            self.data['Images'] = ','.join(self.images)

    def add_category(self, category):
        """Add a category to the product"""
        if category:
            current_cats = self.data['Categories'].split('|') if self.data['Categories'] else []
            if category not in current_cats:
                current_cats.append(category)
                self.data['Categories'] = '|'.join(current_cats)

    def set_stock(self, stock_status, quantity=None):
        """Set stock information"""
        self.data['In stock?'] = 'yes' if stock_status else 'no'
        if quantity is not None:
            self.data['Stock'] = str(quantity)

    def generate_short_description(self, description):
        """Generate short description from full description"""
        if not description:
            return ""
        
        # Split by sentences and take first 2 sentences or first 150 chars
        sentences = re.split(r'[.!?]+', description)
        short_desc = '. '.join(sentence.strip() for sentence in sentences[:2] if sentence.strip())
        
        if len(short_desc) > 150:
            short_desc = short_desc[:147] + "..."
        
        return short_desc

    def to_dict(self):
        """Convert to dictionary format"""
        return self.data

def clean_html(text):
    """Remove HTML tags from text"""
    if not text:
        return ""
    return re.sub(r'<[^>]+>', '', text)

def translate_text(text, from_lang='zh', to_lang='en'):
    """Translate text using multiple translation services"""
    if not text or not text.strip():
        return text
    
    try:
        # Clean the text first
        text = text.strip()
        
        # For Arabic translation, use a more reliable approach
        if to_lang == 'ar':
            return translate_to_arabic(text, from_lang)
        elif to_lang == 'en':
            return translate_to_english(text, from_lang)
        else:
            # For other languages, use the original method
            return translate_to_english(text, from_lang)
            
    except Exception as e:
        log(f"Translation error: {str(e)}", "WARNING")
        return text

def translate_to_arabic(text, from_lang='zh'):
    """Translate text to proper Arabic with correct spacing and grammar"""
    if not text or not text.strip():
        return text
    
    try:
        # First, try to extract meaningful content from HTML if present
        if '<' in text and '>' in text:
            soup = BeautifulSoup(text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # For product names, create a proper Arabic translation
        if len(text) < 200:  # Likely a product name
            return translate_product_name_to_arabic(text)
        else:
            # For descriptions, create a proper Arabic description
            return create_proper_arabic_description(text)
            
    except Exception as e:
        log(f"Arabic translation error: {str(e)}", "WARNING")
        return text

def translate_product_name_to_arabic(text):
    """Directly translate the product name to Arabic using Google Translate."""
    if not text or len(text.strip()) < 2:
        return "منتج عالي الجودة"
    
    try:
        # Try multiple translation methods
        translated = None
        
        # Method 1: Try translate_text
        try:
            translated = ts.translate_text(text, from_language='zh', to_language='ar')
            if translated and isinstance(translated, str) and len(translated.strip()) > 2:
                return translated.strip()
        except Exception as e:
            log(f"translate_text failed: {str(e)}", "DEBUG")
            pass
        
        # Method 2: Try google translate
        if not translated:
            try:
                translated = ts.google(text, from_language='zh', to_language='ar')
                if translated and isinstance(translated, str) and len(translated.strip()) > 2:
                    return translated.strip()
            except Exception as e:
                log(f"google translate failed: {str(e)}", "DEBUG")
                pass
        
        # Method 3: Try bing translate
        if not translated:
            try:
                translated = ts.bing(text, from_language='zh', to_language='ar')
                if translated and isinstance(translated, str) and len(translated.strip()) > 2:
                    return translated.strip()
            except Exception as e:
                log(f"bing translate failed: {str(e)}", "DEBUG")
                pass
        
        if translated and len(translated.strip()) > 2:
            return translated.strip()
        else:
            # Fallback: analyze content and generate appropriate name
            info = analyze_product_content(text)
            if info.get('category'):
                category_names = {
                    'electronics': 'إلكترونيات عالية الجودة',
                    'clothing': 'ملابس عالية الجودة',
                    'home': 'منتجات منزلية عالية الجودة',
                    'toys': 'ألعاب عالية الجودة',
                    'beauty': 'منتجات تجميل عالية الجودة',
                    'sports': 'معدات رياضية عالية الجودة',
                    'books': 'كتب عالية الجودة',
                    'kitchen': 'أدوات مطبخ عالية الجودة'
                }
                return category_names.get(info['category'], 'منتج عالي الجودة')
            return "منتج عالي الجودة"
    except Exception as e:
        log(f"Arabic name translation error: {str(e)}", "WARNING")
        return "منتج عالي الجودة"

def translate_product_name_to_english(text):
    """Directly translate the product name to English using Google Translate."""
    if not text or len(text.strip()) < 2:
        return "High-Quality Product"
    
    try:
        # Try multiple translation methods
        translated = None
        
        # Method 1: Try translate_text
        try:
            translated = ts.translate_text(text, from_language='zh', to_language='en')
            if translated and isinstance(translated, str) and len(translated.strip()) > 2:
                return translated.strip()
        except Exception as e:
            log(f"translate_text failed: {str(e)}", "DEBUG")
            pass
        
        # Method 2: Try google translate
        if not translated:
            try:
                translated = ts.google(text, from_language='zh', to_language='en')
                if translated and isinstance(translated, str) and len(translated.strip()) > 2:
                    return translated.strip()
            except Exception as e:
                log(f"google translate failed: {str(e)}", "DEBUG")
                pass
        
        # Method 3: Try bing translate
        if not translated:
            try:
                translated = ts.bing(text, from_language='zh', to_language='en')
                if translated and isinstance(translated, str) and len(translated.strip()) > 2:
                    return translated.strip()
            except Exception as e:
                log(f"bing translate failed: {str(e)}", "DEBUG")
                pass
        
        if translated and len(translated.strip()) > 2:
            return translated.strip()
        else:
            # Fallback: analyze content and generate appropriate name
            info = analyze_product_content(text)
            if info.get('category'):
                category_names = {
                    'electronics': 'High-Quality Electronics',
                    'clothing': 'High-Quality Clothing',
                    'home': 'High-Quality Home Products',
                    'toys': 'High-Quality Toys',
                    'beauty': 'High-Quality Beauty Products',
                    'sports': 'High-Quality Sports Equipment',
                    'books': 'High-Quality Books',
                    'kitchen': 'High-Quality Kitchen Tools'
                }
                return category_names.get(info['category'], 'High-Quality Product')
            return "High-Quality Product"
    except Exception as e:
        log(f"English name translation error: {str(e)}", "WARNING")
        return "High-Quality Product"

def analyze_product_content(text):
    """Analyze Chinese product content to extract real product information"""
    if not text:
        return {}
    
    info = {}
    text_lower = text.lower()
    
    # Product categories detection
    categories = {
        'electronics': ['手机', '电脑', '平板', '耳机', '充电器', '数据线', 'phone', 'computer', 'tablet', 'headphone', 'charger', 'cable'],
        'clothing': ['衣服', '裤子', '鞋子', '帽子', '包', 'clothes', 'pants', 'shoes', 'hat', 'bag'],
        'home': ['家具', '装饰', '厨房', '浴室', 'furniture', 'decoration', 'kitchen', 'bathroom'],
        'toys': ['玩具', '游戏', '模型', 'toy', 'game', 'model'],
        'beauty': ['化妆品', '护肤品', '香水', 'cosmetic', 'skincare', 'perfume'],
        'sports': ['运动', '健身', '户外', 'sport', 'fitness', 'outdoor'],
        'automotive': ['汽车', '摩托车', '配件', 'car', 'motorcycle', 'accessory'],
        'jewelry': ['珠宝', '手表', '项链', '戒指', 'jewelry', 'watch', 'necklace', 'ring'],
        'books': ['书', '杂志', 'book', 'magazine'],
        'food': ['食品', '饮料', '零食', 'food', 'drink', 'snack']
    }
    
    # Detect category
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            info['category'] = category
            break
    
    # Extract specific product features
    features = {
        'wireless': ['无线', '蓝牙', 'wifi', 'wireless', 'bluetooth'],
        'portable': ['便携', '移动', 'portable', 'mobile'],
        'waterproof': ['防水', 'waterproof', 'water-resistant'],
        'smart': ['智能', 'smart'],
        'led': ['led', '发光'],
        'usb': ['usb', '接口'],
        'battery': ['电池', 'battery'],
        'high_quality': ['高品质', '优质', 'high quality', 'premium'],
        'new': ['新款', '新品', 'new'],
        'hot': ['热销', '热门', 'hot', 'popular']
    }
    
    detected_features = []
    for feature, keywords in features.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_features.append(feature)
    
    info['features'] = detected_features
    
    # Extract size/weight information
    size_patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:cm|厘米)',
        r'(\d+(?:\.\d+)?)\s*(?:inch|英寸)',
        r'(\d+(?:\.\d+)?)\s*(?:kg|千克)',
        r'(\d+(?:\.\d+)?)\s*(?:g|克)',
        r'(\d+(?:\.\d+)?)\s*(?:m|米)'
    ]
    
    for pattern in size_patterns:
        match = re.search(pattern, text)
        if match:
            info['size'] = match.group(1)
            break
    
    # Extract color information
    colors = ['红色', '蓝色', '绿色', '黄色', '黑色', '白色', '粉色', '紫色', '橙色', '灰色',
              'red', 'blue', 'green', 'yellow', 'black', 'white', 'pink', 'purple', 'orange', 'gray']
    
    for color in colors:
        if color in text_lower:
            info['color'] = color
            break
    
    # Extract brand information (common patterns)
    brand_patterns = [
        r'品牌[：:]\s*([^\s,，。]+)',
        r'brand[：:]\s*([^\s,，。]+)',
        r'([A-Z]{2,}[A-Za-z0-9]*)\s*(?:品牌|brand)',
    ]
    
    for pattern in brand_patterns:
        match = re.search(pattern, text)
        if match:
            info['brand'] = match.group(1)
            break
    
    return info

def create_proper_arabic_description(text):
    """Mix: Start with translated original description, then append generated template."""
    try:
        # Analyze product content first
        product_info = analyze_product_content(text)
        
        # Try multiple translation methods for the original description
        translated_desc = ""
        if text and len(text.strip()) > 5:
            try:
                # Method 1: Try translate_text
                translated_desc = ts.translate_text(text, from_language='zh', to_language='ar')
                if translated_desc and isinstance(translated_desc, str) and len(translated_desc.strip()) > 10:
                    log(f"Successfully translated with translate_text: {len(translated_desc)} characters")
            except Exception as e:
                log(f"translate_text failed: {str(e)}", "DEBUG")
                try:
                    # Method 2: Try google translate
                    translated_desc = ts.google(text, from_language='zh', to_language='ar')
                    if translated_desc and isinstance(translated_desc, str) and len(translated_desc.strip()) > 10:
                        log(f"Successfully translated with google: {len(translated_desc)} characters")
                except Exception as e:
                    log(f"google translate failed: {str(e)}", "DEBUG")
                    try:
                        # Method 3: Try bing translate
                        translated_desc = ts.bing(text, from_language='zh', to_language='ar')
                        if translated_desc and isinstance(translated_desc, str) and len(translated_desc.strip()) > 10:
                            log(f"Successfully translated with bing: {len(translated_desc)} characters")
                    except Exception as e:
                        log(f"bing translate failed: {str(e)}", "DEBUG")
        
        description_parts = []
        
        # Add translated description if available
        if translated_desc and len(translated_desc.strip()) > 10:
            description_parts.append(translated_desc.strip())
        
        # Only keep pure translated content - no generated category or feature descriptions
        
        # Only keep pure translated content - no generated specifications
        
        # Only keep translated content - no generic features or additional information
        
        result = "\n".join([part for part in description_parts if part])
        if not result or len(result.strip()) < 10:
            log("No valid translated content available, returning empty description", "WARNING")
            return ""
        return result
    except Exception as e:
        log(f"Arabic description creation error: {str(e)}", "WARNING")
        return ""

def create_proper_english_description(text):
    """Mix: Start with translated original description, then append generated template."""
    try:
        # Analyze product content first
        product_info = analyze_product_content(text)
        
        # Try multiple translation methods for the original description
        translated_desc = ""
        if text and len(text.strip()) > 5:
            try:
                # Method 1: Try translate_text
                translated_desc = ts.translate_text(text, from_language='zh', to_language='en')
                if translated_desc and isinstance(translated_desc, str) and len(translated_desc.strip()) > 10:
                    log(f"Successfully translated with translate_text: {len(translated_desc)} characters")
            except Exception as e:
                log(f"translate_text failed: {str(e)}", "DEBUG")
                try:
                    # Method 2: Try google translate
                    translated_desc = ts.google(text, from_language='zh', to_language='en')
                    if translated_desc and isinstance(translated_desc, str) and len(translated_desc.strip()) > 10:
                        log(f"Successfully translated with google: {len(translated_desc)} characters")
                except Exception as e:
                    log(f"google translate failed: {str(e)}", "DEBUG")
                    try:
                        # Method 3: Try bing translate
                        translated_desc = ts.bing(text, from_language='zh', to_language='en')
                        if translated_desc and isinstance(translated_desc, str) and len(translated_desc.strip()) > 10:
                            log(f"Successfully translated with bing: {len(translated_desc)} characters")
                    except Exception as e:
                        log(f"bing translate failed: {str(e)}", "DEBUG")
        
        description_parts = []
        
        # Add translated description if available
        if translated_desc and len(translated_desc.strip()) > 10:
            description_parts.append(translated_desc.strip())
        
        # Only keep pure translated content - no generated category or feature descriptions
        
        # Only keep pure translated content - no generated specifications
        
        # Only keep translated content - no generic features or additional information
        
        result = "\n".join([part for part in description_parts if part])
        if not result or len(result.strip()) < 10:
            log("No valid translated content available, returning empty description", "WARNING")
            return ""
        return result
    except Exception as e:
        log(f"English description creation error: {str(e)}", "WARNING")
        return ""

def translate_chunk_to_arabic(text, from_lang='zh'):
    """This function is now deprecated - use translate_to_arabic instead"""
    return translate_to_arabic(text, from_lang)

def create_generic_arabic_description(text):
    """This function is now deprecated - use create_proper_arabic_description instead"""
    return create_proper_arabic_description(text)

def translate_to_english(text, from_lang='zh'):
    """Translate text to proper English with correct spacing and grammar"""
    if not text or not text.strip():
        return text

    try:
        # First, try to extract meaningful content from HTML if present
        if '<' in text and '>' in text:
            soup = BeautifulSoup(text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # For product names, create a proper English translation
        if len(text) < 200:  # Likely a product name
            return translate_product_name_to_english(text)
        else:
            # For descriptions, create a proper English description
            return create_proper_english_description(text)
            
    except Exception as e:
        log(f"English translation error: {str(e)}", "WARNING")
        return text

def translate_chunk_to_english(text, from_lang='zh'):
    """This function is now deprecated - use translate_to_english instead"""
    return translate_to_english(text, from_lang)

def create_generic_english_description(text):
    """This function is now deprecated - use create_proper_english_description instead"""
    return create_proper_english_description(text)

def fetch_page_with_cloudscraper(url):
    """Fetch a page using cloudscraper to bypass anti-scraping measures"""
    try:
        log(f"Fetching page: {url}")
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.1688.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        response = scraper.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            log(f"Successfully fetched page (status code: {response.status_code})")
            return response.text
        else:
            log(f"Failed to fetch page (status code: {response.status_code})", "WARNING")
            return None
    except Exception as e:
        log(f"Error fetching page: {str(e)}", "ERROR")
        return None

def extract_product_info(html_content, url, scraping_delay=2):
    """Extract product information from HTML content"""
    try:
        log("Extracting product info from HTML content...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # --- Product Name ---
        product_name = None
        # Try to extract from #productTitle h1
        title_h1 = soup.select_one('#productTitle h1')
        if title_h1 and title_h1.text.strip():
            product_name = title_h1.text.strip()
            log(f"Found product name from #productTitle h1: {product_name}")
        # Fallback to previous logic if not found
        if not product_name:
            title_tag = soup.find('title')
            if title_tag and title_tag.text:
                title_text = title_tag.text.strip()
                if '-' in title_text:
                    product_name = title_text.split('-')[0].strip()
                else:
                    product_name = title_text
                log(f"Found product name from title tag")
        
        # --- Product Images ---
        images = []
        
        # 1. Primary method: Extract from JSON data structures (most reliable)
        json_images = extract_images_from_1688_json(html_content)
        if json_images:
            images = json_images
            log(f"Extracted {len(images)} images from JSON data structures.")
        
        # 2. Fallback: Main gallery images (od-gallery-img)
        if not images:
            gallery_imgs = soup.select('div.od-gallery-turn-item-wrapper img.od-gallery-img')
            for img in gallery_imgs:
                src = img.get('src')
                if src and 'video' not in src and 'icon' not in src and 'placeholder' not in src and src not in images:
                    images.append(src)
            log(f"Fallback: Extracted {len(images)} images from gallery selectors.")
        
        # 3. Fallback: Preview images (ant-image-img preview-img)
        if not images:
            preview_imgs = soup.select('img.ant-image-img.preview-img')
            for img in preview_imgs:
                src = img.get('src')
                if src and 'video' not in src and 'icon' not in src and 'placeholder' not in src and src not in images:
                    images.append(src)
            log(f"Fallback: Extracted {len(images)} images from preview selectors.")
        
        # 4. Fallback: use extract_images_from_1688 for more sources if still no images found
        if not images:
            images = extract_images_from_1688(html_content, soup)
            log(f"Fallback: Extracted {len(images)} images using extract_images_from_1688.")

        # 5. Fallback: use placeholder if still no images found
        if not images:
            images = ["https://via.placeholder.com/800x800?text=No+Image+Available"]
            log("No images found, using placeholder image.")
        
        # Remove duplicates and log final count
        images = list(dict.fromkeys(images))
        log(f"Final image count: {len(images)}")

        # --- Product Description ---
        description_html = None
        
        # 1. Primary method: Extract from featureAttributes JSON data
        feature_description = extract_description_from_feature_attributes(html_content)
        if feature_description:
            description_html = feature_description
            log(f"Extracted description from featureAttributes: {len(feature_description)} characters")
        
        # 2. Try all likely selectors and concatenate all matching blocks
        if not description_html:
            desc_selectors = [
                '#description .html-description',
                '#description .module-od-product-description',
                '.desc-content',
                '#description',
            ]
            desc_blocks = []
            for selector in desc_selectors:
                blocks = soup.select(selector)
                for block in blocks:
                    block_html = str(block)
                    if block_html and len(block_html) > 100:
                        desc_blocks.append(block_html)
            if desc_blocks:
                description_html = '\n'.join(desc_blocks)
                log(f"Found and concatenated {len(desc_blocks)} description blocks from selectors.")
        
        # 3. Try detailUrl with retries and shorter timeout if no HTML found
        if not description_html:
            detail_url_match = re.search(r'"detailUrl"\s*:\s*"([^"]+)",?', html_content)
            if detail_url_match:
                detail_url = detail_url_match.group(1)
                log(f"Found detailUrl for description: {detail_url}")
                max_retries = 2  # Reduced from 3 to 2
                for attempt in range(max_retries):
                    try:
                        resp = requests.get(detail_url, timeout=10)  # Reduced from 30 to 10 seconds
                        if resp.status_code == 200 and len(resp.text) > 100:
                            # Save detailUrl content for debugging
                            try:
                                detail_file = os.path.join(OUTPUT_DIR, f"detail_content_{hash(url)}.html")
                                with open(detail_file, "w", encoding="utf-8") as f:
                                    f.write(resp.text)
                                log(f"Saved detailUrl content to: {detail_file}")
                            except Exception as e:
                                log(f"Failed to save detailUrl content: {e}", "WARNING")
                            # Extract description from the fetched content
                            detail_description = extract_description_from_detail_url(resp.text)
                            if detail_description:
                                description_html = detail_description
                                log(f"Successfully extracted description from detailUrl content (attempt {attempt+1})")
                                break
                            else:
                                log(f"detailUrl content fetched but no description extracted (attempt {attempt+1})")
                        else:
                            log(f"detailUrl fetch attempt {attempt+1} failed: status {resp.status_code}")
                    except Exception as e:
                        log(f"Failed to fetch detailUrl (attempt {attempt+1}): {e}", "WARNING")
                        if attempt == max_retries - 1:  # Last attempt
                            log("Skipping detailUrl fetch, will use fallback description methods", "INFO")
                    time.sleep(1)  # Reduced delay from scraping_delay to 1 second
        
        # 4. Fallback: largest visible HTML/text block
        if not description_html:
            candidates = soup.find_all(['div', 'section'], recursive=True)
            best_block = None
            best_len = 0
            for c in candidates:
                c_html = str(c)
                c_len = len(c_html)
                if c_len > best_len and c_len > 200 and ('img' in c_html or len(c.get_text(strip=True)) > 100):
                    best_block = c_html
                    best_len = c_len
            if best_block:
                description_html = best_block
                log("Used fallback: largest visible HTML/text block")
        
        # 5. Fallback: all <p> tags concatenated (no truncation)
        if not description_html:
            paragraphs = soup.find_all('p')
            all_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            if all_text:
                description_html = all_text
                log("Used fallback: all <p> tags concatenated as description")
        
        # 6. Log and save raw HTML if all fail
        if not description_html:
            description_html = "No description available."
            log("No product description found, using fallback.")
            try:
                with open(os.path.join(OUTPUT_DIR, f"failed_product_{hash(url)}.html"), "w", encoding="utf-8") as f:
                    f.write(html_content)
                log(f"Saved raw HTML for failed product: failed_product_{hash(url)}.html", "WARNING")
            except Exception as e:
                log(f"Failed to save raw HTML: {e}", "WARNING")

        # --- Product Price ---
        price = None
        price_span = soup.select_one('#mainPrice .price-info.currency')
        if price_span:
            price_text = ''.join(price_span.stripped_strings)
            price = price_text.replace('¥', '').strip()
            log(f"Found price from #mainPrice: {price}")
        # Fallback: regex
        if not price:
            price_pattern = r'"price":"([^"]+)"'
            price_matches = re.findall(price_pattern, html_content)
            if price_matches:
                price = price_matches[0]
                log(f"Found price via regex: {price}")
        if not price:
            price = '0'
            log("No price found, using fallback 0.")

        # --- Product Attributes ---
        attributes = {}
        attr_table = soup.select_one('#productAttributes table')
        if attr_table:
            for row in attr_table.select('tr'):
                ths = row.select('th')
                tds = row.select('td')
                for th, td in zip(ths, tds):
                    key = th.get_text(strip=True)
                    value = td.get_text(strip=True)
                    attributes[key] = value
            log(f"Extracted {len(attributes)} product attributes.")

        # Return all extracted info
        return {
            'name': product_name,
            'description': description_html,
            'price': price,
            'images': images,
            'attributes': attributes,
            'url': url
        }
    except Exception as e:
        log(f"Error extracting product info: {str(e)}", "ERROR")
        return None

def clean_description(description):
    """Clean unwanted text from product descriptions while preserving HTML structure"""
    if not description:
        return ""

    # If description contains HTML tables, preserve the structure
    if '<table' in description and '</table>' in description:
        # For HTML descriptions, only remove very specific unwanted patterns
        # Remove CSS styles that might interfere
        description = re.sub(r'<style[^>]*>.*?</style>', '', description, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove local WordPress image URLs
        description = re.sub(r'http://mikel\.local/wp-content/.*?\.(?:png|jpg|jpeg|gif|webp)\b', '', description, flags=re.IGNORECASE)
        
        # Remove very specific unwanted patterns but preserve table structure
        unwanted_patterns = [
            r'(?i)1688\.com',
            r'(?i)alibaba\.com',
            r'(?i)taobao\.com',
            r'(?i)tmall\.com',
            r'(?i)aliexpress\.com'
        ]
        
        for pattern in unwanted_patterns:
            description = re.sub(pattern, '', description)
        
        # Clean up extra whitespace but preserve HTML structure
        description = re.sub(r'\s+', ' ', description)
        description = description.strip()
        
        return description
    
    else:
        # For plain text descriptions, use the original cleaning logic
        # Remove CSS styles
        description = re.sub(r'<style[^>]*>.*?</style>', '', description, flags=re.DOTALL)

        # Remove local WordPress image URLs
        description = re.sub(r'http://mikel\.local/wp-content/.*?\.(?:png|jpg|jpeg|gif|webp)\b', '', description, flags=re.IGNORECASE)

        # Check if this is a structured description (contains | separators)
        is_structured = '|' in description
        
        # Common Alibaba-related patterns to remove (only for non-structured descriptions)
        if not is_structured:
            patterns_to_remove = [
                r'(?i)1688\.com',
                r'(?i)alibaba\.com',
                r'(?i)taobao\.com',
                r'(?i)tmall\.com',
                r'(?i)aliexpress\.com',
                r'(?i)made in china',
                r'(?i)china wholesale',
                r'(?i)chinese supplier'
            ]
            
            for pattern in patterns_to_remove:
                description = re.sub(pattern, '', description)
        
        # Clean up extra whitespace and punctuation
        description = re.sub(r'\s+', ' ', description)
        description = re.sub(r'[^\w\s\-\.\,\|\:\;\(\)\[\]\{\}\<\>\"\']+', '', description)
        description = description.strip()
        
        return description

def check_description_quality(description, language):
    """Check the quality of translated description"""
    if not description:
        return False, "Empty description"
    
    # Check for Chinese characters in non-Chinese output
    if language != 'zh':
        chinese_chars = sum(1 for char in description if '\u4e00' <= char <= '\u9fff')
        if chinese_chars > len(description) * 0.3:  # More than 30% Chinese characters
            return False, f"Too many Chinese characters ({chinese_chars}) in {language} output"
    
    # Check for Arabic characters in Arabic output
    if language == 'ar':
        arabic_chars = sum(1 for char in description if '\u0600' <= char <= '\u06ff' or '\u0750' <= char <= '\u077f')
        if arabic_chars < len(description) * 0.1:  # Less than 10% Arabic characters
            return False, f"Too few Arabic characters ({arabic_chars}) in Arabic output"
    
    # Check for English characters in English output
    if language == 'en':
        english_chars = sum(1 for char in description if char.isalpha() and ord(char) < 128)
        if english_chars < len(description) * 0.3:  # Less than 30% English characters
            return False, f"Too few English characters ({english_chars}) in English output"
    
    # Check for very short descriptions
    if len(description.strip()) < 10:
        return False, "Description too short"
    
    # Check for repetitive patterns (but be more lenient)
    # Count unique characters vs total length
    unique_chars = len(set(description.lower()))
    if unique_chars < len(description) * 0.2 and len(description) > 100:  # More lenient threshold
        return False, "Too many repeated characters"
    
    # Check for repetitive words
    words = description.split()
    if len(words) > 10:
        unique_words = len(set(words))
        if unique_words < len(words) * 0.3:  # Less than 30% unique words
            return False, "Too many repeated words"
    
    return True, "Description quality OK"

def process_product_for_woocommerce(product_info, html_content, url, language='en'):
    """Process product data for WooCommerce import"""
    try:
        woo_product = WooCommerceProduct()
        
        # Extract basic product information
        name = (product_info.get('name') or '').strip()
        description = (product_info.get('description') or '').strip()
        category = (product_info.get('category') or '').strip()
        price = (product_info.get('price') or '0').strip()
        images = [img for img in product_info.get('images', []) if img and isinstance(img, str)]
        
        # Debug: Log the raw description
        if not description:
            log(f"No description found for product: {name}", "INFO")
        else:
            log(f"Raw description length: {len(description)} characters", "INFO")
            log(f"Raw description: {description[:200]}...", "INFO")
        
        # Check if description contains HTML tables
        is_html_description = '<table' in description and '</table>' in description
        
        # Translate content to the specified language
        translated_name = translate_text(name, 'zh', language)
        
        if is_html_description:
            # For HTML descriptions, extract text content and translate it
            log(f"Extracting text from HTML for translation", "INFO")
            # Use BeautifulSoup to extract text content
            soup = BeautifulSoup(description, 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)
            # Clean up extra whitespace
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            log(f"Extracted text content: {text_content[:200]}...", "INFO")
            # Translate the extracted text
            translated_description = translate_text(text_content, 'zh', language)
            log(f"Translated HTML content to {language}", "INFO")
        else:
            # For plain text descriptions, translate normally
            translated_description = translate_text(description, 'zh', language)
        
        # Debug: Log the translated description
        if translated_description:
            log(f"Translated description length: {len(translated_description)} characters", "INFO")
            log(f"Translated description: {translated_description[:200]}...", "INFO")
        else:
            log(f"No translated description available", "INFO")
        
        # Clean the translated description
        cleaned_description = clean_description(translated_description)
        
        # Debug: Log the cleaned description
        if cleaned_description:
            log(f"Cleaned description length: {len(cleaned_description)} characters", "INFO")
            log(f"Cleaned description: {cleaned_description[:200]}...", "INFO")
        else:
            log("Cleaning resulted in empty description", "INFO")
        
        # Check description quality
        quality_ok, quality_message = check_description_quality(cleaned_description, language)
        if not quality_ok:
            log(f"⚠️ Description quality issue: {quality_message}", "WARNING")
            # Try to improve the description
            if language == 'ar' and 'chinese' in quality_message.lower():
                log("🔄 Attempting to retranslate to Arabic...", "INFO")
                # Force retranslation to Arabic
                retry_description = translate_text(description, 'zh', 'ar')
                cleaned_description = clean_description(retry_description)
                quality_ok, quality_message = check_description_quality(cleaned_description, language)
                if quality_ok:
                    log("✅ Retranslation successful", "INFO")
                else:
                    log(f"❌ Retranslation failed: {quality_message}", "WARNING")
            elif language == 'en' and 'chinese' in quality_message.lower():
                log("🔄 Attempting to retranslate to English...", "INFO")
                # Force retranslation to English
                retry_description = translate_text(description, 'zh', 'en')
                cleaned_description = clean_description(retry_description)
                quality_ok, quality_message = check_description_quality(cleaned_description, language)
                if quality_ok:
                    log("✅ Retranslation successful", "INFO")
                else:
                    log(f"❌ Retranslation failed: {quality_message}", "WARNING")
        else:
            log(f"✅ Description quality: {quality_message}", "INFO")
        
        # If we still don't have a description, use only the product name (no generic content)
        if not cleaned_description or cleaned_description.strip() in ('.', '-'):
            log("No valid description found, using only product name", "INFO")
            cleaned_description = translated_name
        
        # Set basic product information with cleaned description
        woo_product.set_basic_info(
            name=translated_name,
            description="",  # Intentionally left blank per user request
            price=price,
            sku=f"1688-{int(time.time())}",
            url=url,
            short_description=""  # Intentionally left blank per user request
        )
        
        # Add category
        woo_product.add_category("Imported Products")
        
        # Extract additional images from HTML if not enough
        if len(images) < 5:  # Try to get at least 5 images
            additional_images = debug_extract_images_from_1688(html_content, BeautifulSoup(html_content, 'html.parser'), url)
            for img in additional_images:
                if img and img not in images:
                    images.append(img)
            
            log(f"Extracted {len(additional_images)} additional images from HTML")
        
        # Add valid image URLs to the product
        valid_urls = []  # Use a list to preserve order
        for img_url in images:
            if not img_url or not isinstance(img_url, str):
                continue
            # Clean the URL
            clean_url = fix_image_url(img_url)
            if not clean_url or 'http' not in clean_url:
                log(f"Skipping invalid image URL: {img_url[:100]}...", "DEBUG")
                continue
            # Remove any JSON data from the URL
            if '{' in clean_url or '}' in clean_url:
                log(f"Found JSON in URL, attempting to extract clean URL: {clean_url[:100]}...", "DEBUG")
                try:
                    json_data = json.loads(clean_url)
                    if isinstance(json_data, dict):
                        for field in ['url', 'image', 'imageUrl', 'imageURL', 'imgUrl', 'img']:
                            if field in json_data and isinstance(json_data[field], str) and 'http' in json_data[field]:
                                clean_url = json_data[field]
                                clean_url = fix_image_url(clean_url)
                                break
                except (json.JSONDecodeError, TypeError):
                    url_match = re.search(r'https?://[^\s\"\']+', clean_url)
                    if url_match:
                        clean_url = url_match.group(0)
                        clean_url = fix_image_url(clean_url)
            # Final validation
            if clean_url and 'http' in clean_url and clean_url not in valid_urls:
                # Skip local WordPress URLs and specific unwanted images
                if 'mikel.local' in clean_url or any(unwanted in clean_url for unwanted in [
                    '2513066_1964054271.png',
                    '2504865_1964054271.png',
                    '2505772_1964054271.png'
                ]):
                    log(f"Skipping local/unwanted image URL: {clean_url[:100]}...", "DEBUG")
                    continue
                if 'b2b-1702133787_s.jpeg' in clean_url:
                    log(f"Skipping known invalid image URL: {clean_url[:100]}...", "DEBUG")
                    continue
                valid_urls.append(clean_url)
                log(f"Using image URL: {clean_url[:100]}...")
        # Set images as comma-separated string
        woo_product.data['Images'] = ','.join(valid_urls)
        
        log(f"Processed {len(valid_urls)} image URLs for WooCommerce import")
        
        return woo_product.to_dict()
        
    except Exception as e:
        log(f"Error processing product for WooCommerce: {str(e)}", "ERROR")
        return None

def export_to_csv(products, output_file, language='en'):
    """Export products to CSV format for WooCommerce import"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # WooCommerce CSV headers
        headers = [
            'Type', 'SKU', 'Name', 'Published', 'Featured', 'Visibility in catalog',
            'Short description', 'Description', 'Date sale price starts', 'Date sale price ends',
            'Tax status', 'Tax class', 'In stock?', 'Stock', 'Backorders allowed?',
            'Sold individually?', 'Weight (kg)', 'Length (cm)', 'Width (cm)', 'Height (cm)',
            'Allow customer reviews?', 'Purchase note', 'Sale price', 'Regular price',
            'Categories', 'Tags', 'Shipping class', 'Images', 'Download limit',
            'Download expiry days', 'Parent', 'Grouped products', 'Upsells', 'Cross-sells',
            'External URL', 'Button text', 'Position', 'Attribute 1 name', 'Attribute 1 value(s)',
            'Attribute 1 visible', 'Attribute 1 global', 'Attribute 2 name', 'Attribute 2 value(s)',
            'Attribute 2 visible', 'Attribute 2 global', 'Product Link'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for product in products:
                # Clean and prepare description for CSV
                description = product.get('Description', '')
                if description:
                    # Remove HTML tags and convert to plain text for CSV compatibility
                    description = re.sub(r'<[^>]+>', '', description)
                    # Replace HTML entities
                    description = description.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                    # Clean up extra whitespace
                    description = re.sub(r'\s+', ' ', description).strip()
                    
                    # Translate the stripped plain text description if it contains Chinese characters
                    if description and any('\u4e00' <= char <= '\u9fff' for char in description):
                        try:
                            translated_desc = translate_text(description, 'zh', language)
                            if translated_desc and translated_desc != description:
                                description = translated_desc
                                log(f"Translated description for CSV export to {language}: {len(description)} characters")
                        except Exception as e:
                            log(f"Translation failed during CSV export: {str(e)}", "WARNING")
                
                # Prepare short description (first 200 characters)
                short_description = description[:200] + '...' if len(description) > 200 else description
                
                # Clean product name
                name = product.get('Name', '')
                if name:
                    name = re.sub(r'<[^>]+>', '', name)
                    name = name.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
                
                # Prepare images string
                images = product.get('Images', '')
                if images:
                    # Split by comma and clean up
                    image_list = [img.strip() for img in images.split(',') if img.strip()]
                    images_str = ','.join(image_list)
                else:
                    images_str = ''
                
                # Create row data
                row = [
                    product.get('Type', 'simple'),  # Type
                    product.get('SKU', ''),  # SKU
                    name,  # Name
                    product.get('Published', '1'),  # Published
                    product.get('Featured', '0'),  # Featured
                    product.get('Visibility in catalog', 'visible'),  # Visibility in catalog
                    short_description,  # Short description (always empty)
                    description,  # Description (always empty)
                    product.get('Date sale price starts', ''),  # Date sale price starts
                    product.get('Date sale price ends', ''),  # Date sale price ends
                    product.get('Tax status', 'taxable'),  # Tax status
                    product.get('Tax class', ''),  # Tax class
                    product.get('In stock?', 'yes'),  # In stock?
                    product.get('Stock', ''),  # Stock
                    product.get('Backorders allowed?', '0'),  # Backorders allowed?
                    product.get('Sold individually?', '0'),  # Sold individually?
                    product.get('Weight (kg)', ''),  # Weight (kg)
                    product.get('Length (cm)', ''),  # Length (cm)
                    product.get('Width (cm)', ''),  # Width (cm)
                    product.get('Height (cm)', ''),  # Height (cm)
                    product.get('Allow customer reviews?', '1'),  # Allow customer reviews?
                    product.get('Purchase note', ''),  # Purchase note
                    product.get('Sale price', ''),  # Sale price
                    product.get('Regular price', '0'),  # Regular price
                    product.get('Categories', 'Imported Products'),  # Categories
                    product.get('Tags', ''),  # Tags
                    product.get('Shipping class', ''),  # Shipping class
                    images_str,  # Images
                    product.get('Download limit', ''),  # Download limit
                    product.get('Download expiry days', ''),  # Download expiry days
                    product.get('Parent', ''),  # Parent
                    product.get('Grouped products', ''),  # Grouped products
                    product.get('Upsells', ''),  # Upsells
                    product.get('Cross-sells', ''),  # Cross-sells
                    product.get('External URL', ''),  # External URL
                    product.get('Button text', ''),  # Button text
                    product.get('Position', ''),  # Position
                    product.get('Attribute 1 name', ''),  # Attribute 1 name
                    product.get('Attribute 1 value(s)', ''),  # Attribute 1 value(s)
                    product.get('Attribute 1 visible', ''),  # Attribute 1 visible
                    product.get('Attribute 1 global', ''),  # Attribute 1 global
                    product.get('Attribute 2 name', ''),  # Attribute 2 name
                    product.get('Attribute 2 value(s)', ''),  # Attribute 2 value(s)
                    product.get('Attribute 2 visible', ''),  # Attribute 2 visible
                    product.get('Attribute 2 global', ''),  # Attribute 2 global
                    product.get('Product Link', '')  # Product Link
                ]
                
                writer.writerow(row)
                log(f"Using image URL for import: {image_list[0] if image_list and len(image_list) > 0 else 'No images'}...")
            
            log(f"Processed {len(products)} image URLs for WooCommerce import")
        
        log(f"Successfully exported products to {output_file}")
        
        # Create backup copy
        backup_file = output_file.replace('.csv', f'_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
        shutil.copy2(output_file, backup_file)
        log(f"Created backup copy: {backup_file}")
        
        # Log file size
        file_size = os.path.getsize(output_file) / 1024  # KB
        log(f"Successfully exported {len(products)} products to {output_file} (Size: {file_size:.2f} KB)")
        
    except Exception as e:
        log(f"Error exporting to CSV: {str(e)}", "ERROR")
        raise

def clean_up_temp_files():
    """Clean up temporary files (HTML cleanup disabled for debugging)"""
    try:
        log("Cleaning up temporary files...")
        # Remove HTML files (DISABLED FOR DEBUGGING)
        # html_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith('page_content_') and f.endswith('.html')]
        # for file in html_files:
        #     os.remove(os.path.join(OUTPUT_DIR, file))
        #     log(f"Removed temporary file: {file}")
        # Remove JSON files (except the final WooCommerce output)
        json_files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith('product_data_') and f.endswith('.json')]
        for file in json_files:
            os.remove(os.path.join(OUTPUT_DIR, file))
            log(f"Removed temporary file: {file}")
        log("Cleanup completed successfully")
    except Exception as e:
        log(f"Error during cleanup: {str(e)}", "ERROR")

def read_urls_from_file(filename):
    """Read URLs from a text file, one per line, removing duplicates"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_urls = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                unique_urls.append(url)
        
        if len(unique_urls) < len(urls):
            log(f"Removed {len(urls) - len(unique_urls)} duplicate URLs", "INFO")
        
        return unique_urls
    except Exception as e:
        log(f"Error reading URLs from file: {str(e)}", "ERROR")
        return []

def cleanup_old_data():
    """Clean up old data files before starting a new scrape"""
    try:
        # List of files and directories to clean up
        cleanup_paths = [
            os.path.join(OUTPUT_DIR, 'woocommerce_products.csv'),
            os.path.join(OUTPUT_DIR, 'scraped_data.json'),
            LOGS_DIR
        ]
        
        for path in cleanup_paths:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                    log(f"Removed file: {path}", "DEBUG")
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                    log(f"Removed directory: {path}", "DEBUG")
            except Exception as e:
                log(f"Error cleaning up {path}: {str(e)}", "WARNING")
        
        # Recreate necessary directories
        os.makedirs(LOGS_DIR, exist_ok=True)
        
    except Exception as e:
        log(f"Error in cleanup_old_data: {str(e)}", "ERROR")

def extract_product_data_from_json(html_content):
    """
    Extract real product data from embedded JSON in 1688 HTML pages.
    This is the primary method to get actual product data without generic text.
    """
    try:
        log("Extracting product data from embedded JSON...")
        
        # Look for the main JSON data structure that contains product information
        # This is typically in a script tag with window.runParams or similar
        json_patterns = [
            r'window\.runParams\s*=\s*({.+?});',
            r'window\.detailData\s*=\s*({.+?});',
            r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
            r'window\.productData\s*=\s*({.+?});',
            r'window\.offerData\s*=\s*({.+?});',
            r'window\.data\s*=\s*({.+?});'
        ]
        
        product_data = {}
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html_content, re.DOTALL)
            if matches:
                try:
                    json_data = json.loads(matches[0])
                    log(f"Found JSON data structure with {len(json_data)} top-level keys")
                    
                    # Extract product information from the JSON structure
                    extracted_data = extract_from_json_structure(json_data)
                    if extracted_data:
                        product_data.update(extracted_data)
                        log(f"Successfully extracted data from JSON pattern: {pattern[:50]}...")
                        break
                except json.JSONDecodeError as e:
                    log(f"Failed to parse JSON from pattern {pattern[:50]}...: {e}", "WARNING")
                    continue
        
        # If no JSON found in script tags, try to find JSON in the HTML body
        if not product_data:
            log("No JSON found in script tags, searching HTML body...")
            # Look for JSON-like structures in the HTML
            body_json_patterns = [
                r'"offerDetail":\s*\{([^}]+)\}',
                r'"productInfo":\s*\{([^}]+)\}',
                r'"featureAttributes":\s*\[(.*?)\]',
                r'"mainImageList":\s*\[(.*?)\]',
                r'"offerImgList":\s*\[(.*?)\]',
                r'"imageList":\s*\[(.*?)\]'
            ]
            
            for pattern in body_json_patterns:
                matches = re.findall(pattern, html_content, re.DOTALL)
                if matches:
                    log(f"Found data with pattern: {pattern}")
                    extracted_data = extract_from_body_patterns(pattern, matches)
                    if extracted_data:
                        product_data.update(extracted_data)
        
        log(f"Final extracted data keys: {list(product_data.keys())}")
        return product_data
        
    except Exception as e:
        log(f"Error extracting product data from JSON: {str(e)}", "ERROR")
        return {}

def extract_from_json_structure(json_data):
    """Extract product information from parsed JSON structure"""
    try:
        extracted = {}
        
        # Navigate through the JSON structure to find product data
        # Common paths in 1688 JSON structure
        paths_to_check = [
            ['offerDetail'],
            ['productInfo'],
            ['data', 'offerDetail'],
            ['data', 'productInfo'],
            ['detail', 'offerDetail'],
            ['detail', 'productInfo'],
            ['result', 'offerDetail'],
            ['result', 'productInfo']
        ]
        
        for path in paths_to_check:
            current = json_data
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    current = None
                    break
            
            if current and isinstance(current, dict):
                log(f"Found data at path: {' -> '.join(path)}")
                
                # Extract title
                if 'title' in current and current['title']:
                    extracted['title'] = current['title']
                    log(f"Found title: {current['title'][:50]}...")
                
                # Extract subject (alternative title field)
                if 'subject' in current and current['subject'] and 'title' not in extracted:
                    extracted['title'] = current['subject']
                    log(f"Found subject as title: {current['subject'][:50]}...")
                
                # Extract price
                if 'price' in current and current['price']:
                    extracted['price'] = str(current['price'])
                    log(f"Found price: {current['price']}")
                
                # Extract images
                if 'mainImageList' in current and current['mainImageList']:
                    images = []
                    for img in current['mainImageList']:
                        if isinstance(img, dict) and 'fullPathImageURI' in img:
                            images.append(img['fullPathImageURI'])
                        elif isinstance(img, str):
                            images.append(img)
                    if images:
                        extracted['images'] = images
                        log(f"Found {len(images)} images in mainImageList")
                
                # Extract offerImgList (alternative image field)
                if 'offerImgList' in current and current['offerImgList'] and 'images' not in extracted:
                    images = []
                    for img in current['offerImgList']:
                        if isinstance(img, dict) and 'fullPathImageURI' in img:
                            images.append(img['fullPathImageURI'])
                        elif isinstance(img, str):
                            images.append(img)
                    if images:
                        extracted['images'] = images
                        log(f"Found {len(images)} images in offerImgList")
                
                # Extract imageList (another alternative)
                if 'imageList' in current and current['imageList'] and 'images' not in extracted:
                    images = []
                    for img in current['imageList']:
                        if isinstance(img, dict) and 'fullPathImageURI' in img:
                            images.append(img['fullPathImageURI'])
                        elif isinstance(img, str):
                            images.append(img)
                    if images:
                        extracted['images'] = images
                        log(f"Found {len(images)} images in imageList")
                
                # Extract attributes
                if 'featureAttributes' in current and current['featureAttributes']:
                    attributes = {}
                    for attr in current['featureAttributes']:
                        if isinstance(attr, dict) and 'name' in attr and 'value' in attr:
                            attributes[attr['name']] = attr['value']
                    if attributes:
                        extracted['attributes'] = attributes
                        log(f"Found {len(attributes)} attributes")
                
                # Extract description from detailUrl
                if 'detailUrl' in current and current['detailUrl']:
                    extracted['detailUrl'] = current['detailUrl']
                    log(f"Found detailUrl: {current['detailUrl']}")
                
                # Extract SKU information
                if 'skuProps' in current and current['skuProps']:
                    skus = []
                    for sku in current['skuProps']:
                        if isinstance(sku, dict):
                            sku_info = {}
                            for key, value in sku.items():
                                if key in ['skuId', 'skuIdStr', 'price', 'priceStr', 'canBookCount']:
                                    sku_info[key] = value
                            if sku_info:
                                skus.append(sku_info)
                    if skus:
                        extracted['skus'] = skus
                        log(f"Found {len(skus)} SKU variants")
                
                # Extract company/seller information
                if 'companyName' in current and current['companyName']:
                    extracted['company'] = current['companyName']
                    log(f"Found company: {current['companyName']}")
                
                if 'sellerLoginId' in current and current['sellerLoginId']:
                    extracted['seller'] = current['sellerLoginId']
                    log(f"Found seller: {current['sellerLoginId']}")
                
                # Extract category information
                if 'leafCategoryName' in current and current['leafCategoryName']:
                    extracted['category'] = current['leafCategoryName']
                    log(f"Found category: {current['leafCategoryName']}")
                
                # Extract sales information
                if 'saleCount' in current and current['saleCount']:
                    extracted['sales_count'] = current['saleCount']
                    log(f"Found sales count: {current['saleCount']}")
                
                # Extract unit information
                if 'unit' in current and current['unit']:
                    extracted['unit'] = current['unit']
                    log(f"Found unit: {current['unit']}")
                
                # If we found substantial data, break
                if len(extracted) >= 3:  # At least title, price, and one other field
                    break
        
        return extracted
        
    except Exception as e:
        log(f"Error extracting from JSON structure: {str(e)}", "ERROR")
        return {}

def extract_from_body_patterns(pattern, matches):
    """Extract data from JSON-like patterns found in HTML body"""
    try:
        extracted = {}
        
        for match in matches:
            if pattern == r'"offerDetail":\s*\{([^}]+)\}':
                # Extract from offerDetail
                title_match = re.search(r'"title":\s*"([^"]+)"', match)
                if title_match:
                    extracted['title'] = title_match.group(1)
                
                price_match = re.search(r'"price":\s*"([^"]+)"', match)
                if price_match:
                    extracted['price'] = price_match.group(1)
                
                detail_url_match = re.search(r'"detailUrl":\s*"([^"]+)"', match)
                if detail_url_match:
                    extracted['detailUrl'] = detail_url_match.group(1)
            
            elif pattern == r'"featureAttributes":\s*\[(.*?)\]':
                # Extract attributes
                attributes = {}
                attr_matches = re.findall(r'"name":\s*"([^"]+)"[^}]*"value":\s*"([^"]+)"', match)
                for name, value in attr_matches:
                    attributes[name] = value
                if attributes:
                    extracted['attributes'] = attributes
            
            elif pattern in [r'"mainImageList":\s*\[(.*?)\]', r'"offerImgList":\s*\[(.*?)\]', r'"imageList":\s*\[(.*?)\]']:
                # Extract images
                if 'images' not in extracted:
                    images = []
                    img_matches = re.findall(r'"fullPathImageURI":\s*"([^"]+)"', match)
                    for img_url in img_matches:
                        if 'http' in img_url:
                            images.append(img_url)
                    if images:
                        extracted['images'] = images
        
        return extracted
        
    except Exception as e:
        log(f"Error extracting from body patterns: {str(e)}", "ERROR")
        return {}

def main(scraping_delay=2, language='en'):
    """Main function to run the WooCommerce 1688 scraper"""
    try:
        log("Starting WooCommerce 1688 Scraper...")
        
        # Read language setting from temporary settings file if it exists
        temp_settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp_scraper_settings.json')
        if os.path.exists(temp_settings_path):
            try:
                with open(temp_settings_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    language = settings.get('language', 'en')
                    # The GUI now passes proper language codes ('en', 'ar', 'fr')
                    # so we don't need to convert from language names
                    log(f"Using language: {language}")
            except Exception as e:
                log(f"Error reading settings: {e}", "WARNING")
                language = 'en'
        else:
            log(f"Temp settings file not found at: {temp_settings_path}", "INFO")
            log(f"Using default language: {language}", "INFO")
        
        # Create necessary directories
        # Note: Removed product_images folder creation as it's not needed
        
        # Read URLs from file
        urls = read_urls_from_file('urls.txt')
        if not urls:
            log("No URLs found in urls.txt", "ERROR")
            return
            
        log(f"Found {len(urls)} URLs to process")
        
        all_products = []
        
        for i, current_url in enumerate(urls):
            log(f"\nProcessing URL ({i+1}/{len(urls)}): {current_url}")
            
            # Fetch the page
            html_content = fetch_page_with_cloudscraper(current_url)
            if not html_content:
                log(f"Failed to fetch page: {current_url}", "ERROR")
                continue
            
            # Always save HTML content for debugging
            html_filename = os.path.join(OUTPUT_DIR, f'page_content_{i}.html')
            try:
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                log(f"Saved HTML content to {html_filename}")
            except Exception as e:
                log(f"Failed to save HTML content: {e}", "WARNING")
                
            # Extract product info
            product_info = extract_product_info(html_content, current_url, scraping_delay=scraping_delay)
            if not product_info:
                log(f"Failed to extract product info from: {current_url}", "ERROR")
                continue
                
            # Process for WooCommerce
            log(f"Processing product info: {json.dumps(product_info, ensure_ascii=False, indent=2)}", "DEBUG")
            woocommerce_product = process_product_for_woocommerce(product_info, html_content, current_url, language)
            if woocommerce_product:
                log(f"Successfully processed WooCommerce product: {json.dumps(woocommerce_product, ensure_ascii=False, indent=2)}", "DEBUG")
                all_products.append(woocommerce_product)
            else:
                log("Failed to process product for WooCommerce", "ERROR")
                
        # Save raw product data for debugging
        if all_products:
            log(f"Preparing to export {len(all_products)} products to CSV", "DEBUG")
            
            # Save raw product data
            raw_products_file = os.path.join(OUTPUT_DIR, "raw_products.json")
            with open(raw_products_file, "w", encoding="utf-8") as f:
                json.dump(all_products, f, ensure_ascii=False, indent=2)
            log(f"Saved raw product data to {os.path.abspath(raw_products_file)}")
            
            # Export to CSV for WooCommerce import
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv_filename = f"woocommerce_import_{timestamp}.csv"
            csv_path = os.path.join(OUTPUT_DIR, csv_filename)
            
            # Call export_to_csv with the products list and full path
            export_to_csv(all_products, csv_path, language)
            
            # Verify the file was created
            csv_path = os.path.join(OUTPUT_DIR, csv_filename)
            if os.path.exists(csv_path):
                file_size = os.path.getsize(csv_path) / 1024  # Size in KB
                log(f"Successfully exported {len(all_products)} products to {os.path.abspath(csv_path)} (Size: {file_size:.2f} KB)", "INFO")
            else:
                log(f"Failed to create CSV file: {csv_path}", "ERROR")
        else:
            log("No products were processed successfully", "WARNING")
        
        # Clean up temporary files
        clean_up_temp_files()
        
        log("WooCommerce 1688 Scraper completed!")
        
    except Exception as e:
        log(f"Error in main: {str(e)}", "ERROR")

def run(scraping_delay=2):
    """Entry point for the script"""
    print("\n=== Starting script execution ===")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print("\nChecking for required files...")
    
    # Check if urls.txt exists
    if not os.path.exists('urls.txt'):
        print("Error: urls.txt not found in the current directory")
        return 1
    
    print("[OK] urls.txt found")
    
    try:
        print("\n=== Starting main function ===")
        main(scraping_delay=scraping_delay)
        print("\n=== Main function completed successfully ===")
        return 0
    except Exception as e:
        print(f"\nERROR: Unhandled exception in main function: {str(e)}")
        log(f"\nERROR: Unhandled exception: {str(e)}", "ERROR")
        return 1

if __name__ == "__main__":
    import sys
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--scraping_delay', type=int, default=2, help='Delay between requests in seconds')
    args = parser.parse_args()
    print("Script started...")
    sys.exit(run(scraping_delay=args.scraping_delay))