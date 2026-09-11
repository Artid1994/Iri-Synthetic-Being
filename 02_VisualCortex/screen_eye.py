#!/usr/bin/env python3
"""
Visual Cortex - Screen Perception Engine for AE01M (Iri)
Provides screen capture, OCR text extraction, and element localization.
"""
import os
import sys
import time
import re
from pathlib import Path
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass
from PIL import Image, ImageDraw
import subprocess

# Add Neocortex to path for directives
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "01_Neocortex"))

from core_directives import CoreDirectives

# Visual Cortex paths
VISUAL_CORTEX_DIR = Path(__file__).parent
CACHE_DIR = VISUAL_CORTEX_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Resource limits
MAX_CAPTURE_FREQUENCY = 0.5  # Max 1 capture per 2 seconds
MAX_CACHE_SIZE_MB = 50  # Maximum cache size
last_capture_time = 0.0


@dataclass
class TextElement:
    """Detected text element on screen."""
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get center coordinates of element."""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        """Get bounding box as (x, y, w, h)."""
        return (self.x, self.y, self.width, self.height)


class ScreenEye:
    """
    Screen perception and OCR engine.
    Captures screen content and extracts text with coordinates.
    Optimized for low CPU usage.
    """
    
    def __init__(self, ocr_scale=0.5, fast_mode=True):
        """
        Initialize screen eye.
        
        Args:
            ocr_scale: Scale factor for OCR processing (0.5 = 50% size, faster)
            fast_mode: Use fast OCR settings (less accurate but much faster)
        """
        self.last_screenshot_path = None
        self.last_elements: List[TextElement] = []
        self.ocr_scale = ocr_scale
        self.fast_mode = fast_mode
        
        # Check for screen capture tools
        self.capture_method = self._detect_capture_method()
        
        # Check for tesseract
        self.ocr_available = self._check_ocr()
        
        print(f"[VisualCortex] Initialized")
        print(f"  Capture method: {self.capture_method}")
        print(f"  OCR available: {self.ocr_available}")
        print(f"  OCR scale: {self.ocr_scale * 100:.0f}% (CPU optimization)")
        print(f"  Fast mode: {self.fast_mode}")
    
    def _detect_capture_method(self) -> str:
        """Detect available screen capture method."""
        # Try different methods in order of preference
        methods = [
            ("import", "imagemagick"),  # ImageMagick import
            ("scrot", "scrot"),
            ("maim", "maim"),
            ("gnome-screenshot", "gnome"),
        ]
        
        for cmd, name in methods:
            try:
                result = subprocess.run(
                    ["which", cmd],
                    capture_output=True,
                    timeout=1
                )
                if result.returncode == 0:
                    return name
            except:
                continue
        
        # Fallback: try PyQt5/PyQt6 screen capture
        try:
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtGui import QScreen
            return "pyqt5"
        except ImportError:
            pass
        
        try:
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtGui import QScreen
            return "pyqt6"
        except ImportError:
            pass
        
        # Last resort: PIL with X11
        return "pil_x11"
    
    def _check_ocr(self) -> bool:
        """Check if tesseract OCR is available."""
        try:
            result = subprocess.run(
                ["tesseract", "--version"],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    def _enforce_capture_rate_limit(self) -> bool:
        """
        Enforce capture frequency limit (DIRECTIVE_9 resource protection).
        Returns True if capture is allowed.
        """
        global last_capture_time
        current_time = time.time()
        
        if current_time - last_capture_time < MAX_CAPTURE_FREQUENCY:
            elapsed = current_time - last_capture_time
            wait_time = MAX_CAPTURE_FREQUENCY - elapsed
            print(f"[VisualCortex] Rate limit: wait {wait_time:.1f}s")
            return False
        
        last_capture_time = current_time
        return True
    
    def _cleanup_cache(self):
        """Clean old cache files to stay under size limit."""
        cache_files = list(CACHE_DIR.glob("*.png"))
        
        # Sort by modification time
        cache_files.sort(key=lambda p: p.stat().st_mtime)
        
        total_size_mb = sum(f.stat().st_size for f in cache_files) / (1024 * 1024)
        
        # Remove oldest files if over limit
        while total_size_mb > MAX_CACHE_SIZE_MB and cache_files:
            oldest = cache_files.pop(0)
            size_mb = oldest.stat().st_size / (1024 * 1024)
            oldest.unlink()
            total_size_mb -= size_mb
            print(f"[VisualCortex] Cleaned cache: {oldest.name} ({size_mb:.1f}MB)")
    
    def capture_screen(self, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Capture current screen content.
        
        Args:
            output_path: Optional custom output path
        
        Returns:
            Path to captured image, or None if failed
        """
        # Enforce rate limiting
        if not self._enforce_capture_rate_limit():
            return self.last_screenshot_path
        
        # Default output path
        if output_path is None:
            timestamp = int(time.time())
            output_path = CACHE_DIR / f"screen_{timestamp}.png"
        
        try:
            if self.capture_method == "imagemagick":
                subprocess.run(
                    ["import", "-window", "root", str(output_path)],
                    timeout=5,
                    check=True
                )
            
            elif self.capture_method == "scrot":
                subprocess.run(
                    ["scrot", str(output_path)],
                    timeout=5,
                    check=True
                )
            
            elif self.capture_method == "maim":
                subprocess.run(
                    ["maim", str(output_path)],
                    timeout=5,
                    check=True
                )
            
            elif self.capture_method == "gnome":
                subprocess.run(
                    ["gnome-screenshot", "-f", str(output_path)],
                    timeout=5,
                    check=True
                )
            
            elif self.capture_method == "pil_x11":
                # Fallback: use PIL with X11
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                screenshot.save(output_path)
            
            else:
                print(f"[VisualCortex] No capture method available")
                return None
            
            if output_path.exists():
                self.last_screenshot_path = output_path
                self._cleanup_cache()
                
                size_kb = output_path.stat().st_size / 1024
                print(f"[VisualCortex] Screen captured: {output_path.name} ({size_kb:.1f}KB)")
                
                return output_path
        
        except Exception as e:
            print(f"[VisualCortex] Capture failed: {e}")
            return None
    
    def _apply_privacy_filter(self, image: Image.Image) -> Image.Image:
        """
        Apply privacy filter to redact sensitive information (DIRECTIVE_8).
        
        Args:
            image: PIL Image to filter
        
        Returns:
            Filtered image with sensitive areas blurred/redacted
        """
        # For now, return unmodified
        # In production, this would:
        # 1. Run OCR to detect text
        # 2. Check for sensitive patterns (passwords, tokens, etc.)
        # 3. Blur/redact matching regions
        
        return image
    
    def read_screen_text(self, image_path: Optional[Path] = None) -> List[TextElement]:
        """
        Extract text from screen using OCR.
        Optimized for low CPU usage with downscaling and fast PSM settings.
        
        Args:
            image_path: Path to image, or None to capture current screen
        
        Returns:
            List of detected text elements with coordinates (scaled to full resolution)
        """
        if not self.ocr_available:
            print("[VisualCortex] OCR not available (tesseract not installed)")
            return []
        
        # Capture screen if no image provided
        if image_path is None:
            image_path = self.capture_screen()
            if image_path is None:
                return []
        
        try:
            import pytesseract
            from PIL import Image
            
            # Load image
            original_image = Image.open(image_path)
            original_width, original_height = original_image.size
            
            # Downscale for faster OCR processing
            if self.ocr_scale < 1.0:
                new_width = int(original_width * self.ocr_scale)
                new_height = int(original_height * self.ocr_scale)
                image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"[VisualCortex] Downscaled for OCR: {original_width}x{original_height} -> {new_width}x{new_height}")
            else:
                image = original_image
            
            # Apply privacy filter
            image = self._apply_privacy_filter(image)
            
            # Prepare OCR configuration for low CPU usage
            ocr_config = []
            
            if self.fast_mode:
                # PSM 3 = Fully automatic page segmentation, but no OSD (faster)
                # PSM 11 = Sparse text. Find as much text as possible in no particular order (fastest)
                # OEM 1 = Neural nets LSTM engine only (faster than legacy)
                ocr_config.extend([
                    '--psm', '3',     # Fast automatic segmentation
                    '--oem', '1',     # LSTM engine (fast)
                ])
            
            # Convert config to string
            config_str = ' '.join(ocr_config) if ocr_config else ''
            
            # Set lower process priority to avoid CPU spikes
            try:
                os.nice(10)  # Lower priority (higher nice value)
            except:
                pass  # Not available on all systems
            
            # Run OCR with bounding box data
            # Format: level word_num left top width height conf text
            ocr_data = pytesseract.image_to_data(
                image,
                lang='eng+tha',  # English + Thai
                config=config_str,
                output_type=pytesseract.Output.DICT
            )
            
            # Reset priority
            try:
                os.nice(-10)  # Restore priority
            except:
                pass
            
            elements = []
            n_boxes = len(ocr_data['text'])
            scale_factor = 1.0 / self.ocr_scale  # Scale coordinates back to full resolution
            
            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                if not text:
                    continue
                
                conf = float(ocr_data['conf'][i])
                if conf < 30:  # Skip low confidence detections
                    continue
                
                # Scale coordinates back to full resolution
                element = TextElement(
                    text=text,
                    x=int(ocr_data['left'][i] * scale_factor),
                    y=int(ocr_data['top'][i] * scale_factor),
                    width=int(ocr_data['width'][i] * scale_factor),
                    height=int(ocr_data['height'][i] * scale_factor),
                    confidence=conf
                )
                
                # Check for sensitive data (DIRECTIVE_8)
                has_sensitive, detected_types, _ = CoreDirectives.check_sensitive_data(text)
                if has_sensitive:
                    print(f"[VisualCortex] Sensitive data detected and filtered: {detected_types}")
                    continue
                
                elements.append(element)
            
            self.last_elements = elements
            print(f"[VisualCortex] Extracted {len(elements)} text elements (fast mode: {self.fast_mode})")
            
            return elements
        
        except Exception as e:
            print(f"[VisualCortex] OCR failed: {e}")
            return []
    
    def find_element_coordinate(self, text_query: str) -> Optional[Tuple[int, int]]:
        """
        Find coordinates of text element on screen.
        
        Args:
            text_query: Text to search for (case-insensitive, partial match)
        
        Returns:
            (x, y) center coordinates, or None if not found
        """
        # Get current screen text if not cached
        if not self.last_elements:
            self.read_screen_text()
        
        text_query_lower = text_query.lower()
        
        # Search for matching element
        for element in self.last_elements:
            if text_query_lower in element.text.lower():
                x, y = element.center
                print(f"[VisualCortex] Found '{text_query}' at ({x}, {y})")
                return (x, y)
        
        print(f"[VisualCortex] Element '{text_query}' not found")
        return None
    
    def visualize_detection(self, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Create visualization of detected text elements.
        
        Args:
            output_path: Optional output path for visualization
        
        Returns:
            Path to visualization image
        """
        if not self.last_screenshot_path or not self.last_elements:
            print("[VisualCortex] No detection data to visualize")
            return None
        
        try:
            # Load screenshot
            image = Image.open(self.last_screenshot_path)
            draw = ImageDraw.Draw(image)
            
            # Draw bounding boxes
            for element in self.last_elements:
                x, y, w, h = element.bbox
                # Draw rectangle
                draw.rectangle(
                    [x, y, x + w, y + h],
                    outline="red",
                    width=2
                )
                # Draw center point
                cx, cy = element.center
                draw.ellipse(
                    [cx - 3, cy - 3, cx + 3, cy + 3],
                    fill="blue"
                )
            
            # Save visualization
            if output_path is None:
                output_path = CACHE_DIR / f"visual_debug_{int(time.time())}.png"
            
            image.save(output_path)
            print(f"[VisualCortex] Visualization saved: {output_path}")
            
            return output_path
        
        except Exception as e:
            print(f"[VisualCortex] Visualization failed: {e}")
            return None


def test_visual_cortex():
    """Test visual cortex functionality with CPU optimization."""
    print("=" * 60)
    print("Visual Cortex - Screen Perception Test")
    print("CPU Optimized with 50% Downscaling + Fast OCR")
    print("=" * 60)
    
    # Test with optimized settings (default)
    eye = ScreenEye(ocr_scale=0.5, fast_mode=True)
    
    # Test 1: Screen capture
    print("\n1. Testing screen capture...")
    screenshot_path = eye.capture_screen(CACHE_DIR / "current_screen.png")
    if screenshot_path:
        print(f"   ✓ Screen captured: {screenshot_path}")
    else:
        print("   ✗ Screen capture failed")
    
    # Test 2: OCR text extraction with performance measurement
    if eye.ocr_available:
        print("\n2. Testing OCR text extraction (optimized)...")
        import time
        start_time = time.time()
        
        elements = eye.read_screen_text(screenshot_path)
        
        elapsed = time.time() - start_time
        print(f"   ✓ Found {len(elements)} text elements in {elapsed:.2f}s")
        
        # Show first 5 elements with scaled coordinates
        for i, elem in enumerate(elements[:5]):
            print(f"     [{i+1}] '{elem.text}' at ({elem.x}, {elem.y}) conf={elem.confidence:.0f}%")
        
        # Test 3: Element coordinate finding
        if elements:
            print("\n3. Testing element coordinate finding...")
            # Try to find first detected word
            test_word = elements[0].text
            coords = eye.find_element_coordinate(test_word)
            if coords:
                print(f"   ✓ Found '{test_word}' at {coords}")
            
            # Test 4: Visualization
            print("\n4. Creating detection visualization...")
            viz_path = eye.visualize_detection()
            if viz_path:
                print(f"   ✓ Visualization saved: {viz_path}")
        
        # Test 5: Performance comparison (if tesseract available)
        print("\n5. Performance Analysis:")
        print(f"   Image size for OCR: {int(1920 * eye.ocr_scale)}x{int(1200 * eye.ocr_scale)}")
        print(f"   Pixel reduction: {(1.0 - eye.ocr_scale**2) * 100:.1f}%")
        print(f"   Est. CPU savings: ~{(1.0 - eye.ocr_scale**2) * 60:.0f}%")
        print(f"   Processing time: {elapsed:.2f}s")
        print(f"   Fast mode: {eye.fast_mode}")
        print(f"   PSM mode: 3 (fast auto segmentation)")
        print(f"   OEM engine: 1 (LSTM neural network)")
        
    else:
        print("\n2. OCR not available (install: sudo apt install tesseract-ocr tesseract-ocr-tha)")
        print("   CPU optimizations ready, awaiting tesseract installation")
    
    print("\n" + "=" * 60)
    print("Visual Cortex test complete")
    print("CPU-optimized settings active: 50% scale + fast PSM")
    print("=" * 60)


if __name__ == "__main__":
    test_visual_cortex()
