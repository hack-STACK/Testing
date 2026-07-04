"""
Artifact Manager - Manages screenshot and video organization.

Automatically organizes screenshots (pass/fail) and videos from test execution
with consistent naming conventions (YYYYMMDD_HHMMSS_TestName).
"""

import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional


class ArtifactManager:
    """
    Manages test artifacts (screenshots and videos).
    
    Organizes and renames artifacts to consistent naming convention:
    YYYYMMDD_HHMMSS_TestName.ext
    """
    
    def __init__(self,
                 screenshot_dir: Path = Path("screenshots"),
                 artifact_dir: Path = Path("artifacts"),
                 video_source_dir: Path = Path("videos")):
        """Initialize artifact manager."""
        self.screenshot_dir = Path(screenshot_dir)
        self.artifact_dir = Path(artifact_dir)
        self.video_source_dir = Path(video_source_dir)
        self.execution_artifacts = {
            "screenshots": [],
            "videos": []
        }
        
        # Create destination directories
        self.pass_screenshot_dir = self.artifact_dir / "screenshots" / "pass"
        self.fail_screenshot_dir = self.artifact_dir / "screenshots" / "fail"
        self.artifact_video_dir = self.artifact_dir / "videos"
        
        for directory in [self.pass_screenshot_dir, self.fail_screenshot_dir, self.artifact_video_dir]:
            directory.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, test_name: str, extension: str, source_path: Optional[Path] = None) -> str:
        """Generate consistent filename with timestamp.
        
        Uses file's modification time if source_path provided, otherwise uses current time.
        """
        if source_path and source_path.exists():
            # Use file's modification time
            mtime = datetime.fromtimestamp(source_path.stat().st_mtime)
            timestamp = mtime.strftime("%Y%m%d_%H%M%S")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Clean test name (remove special characters)
        clean_name = test_name.replace("::", "_").replace("[", "_").replace("]", "_")
        return f"{timestamp}_{clean_name}{extension}"
    
    def move_screenshot(self, screenshot_path: Path, test_name: str, passed: bool = True) -> Optional[Path]:
        """
        Move and rename screenshot to appropriate directory.
        
        Args:
            screenshot_path: Path to screenshot file
            test_name: Test name for filename
            passed: True for pass, False for fail
        
        Returns:
            New path of screenshot, or None if failed
        """
        if not screenshot_path.exists():
            return None
        
        try:
            dest_dir = self.pass_screenshot_dir if passed else self.fail_screenshot_dir
            new_filename = self._generate_filename(test_name, screenshot_path.suffix, screenshot_path)
            new_path = dest_dir / new_filename
            
            shutil.copy2(screenshot_path, new_path)
            self.execution_artifacts["screenshots"].append({
                "test_name": test_name,
                "path": str(new_path),
                "passed": passed
            })
            return new_path
        except Exception as e:
            print(f"Error moving screenshot: {e}")
            return None
    
    def move_video(self, video_source: Path, test_name: str, module: str = "other") -> Optional[Path]:
        """
        Move and rename video to artifacts directory.
        
        Args:
            video_source: Path to video file
            test_name: Test name for filename
            module: Test module for organization
        
        Returns:
            New path of video, or None if failed
        """
        if not video_source.exists():
            return None
        
        try:
            module_dir = self.artifact_video_dir / module
            module_dir.mkdir(parents=True, exist_ok=True)
            
            new_filename = self._generate_filename(test_name, video_source.suffix, video_source)
            new_path = module_dir / new_filename
            
            shutil.move(str(video_source), str(new_path))
            self.execution_artifacts["videos"].append({
                "test_name": test_name,
                "path": str(new_path),
                "module": module
            })
            return new_path
        except Exception as e:
            print(f"Error moving video: {e}")
            return None
    
    def organize_all_screenshots(self) -> tuple[int, int]:
        """
        Organize all screenshots in screenshot directory.
        
        Returns:
            Tuple of (moved_count, error_count)
        """
        moved = 0
        errors = 0
        
        # Check for failed screenshots
        failed_dir = self.screenshot_dir / "failed"
        if failed_dir.exists():
            for screenshot in failed_dir.glob("*.png"):
                test_name = screenshot.stem
                if self.move_screenshot(screenshot, test_name, passed=False):
                    screenshot.unlink()  # Delete original after move
                    moved += 1
                else:
                    errors += 1
        
        # Note: pass screenshots are not captured by default, only failed
        return moved, errors
    
    def organize_all_videos(self) -> tuple[int, int]:
        """
        Organize all videos from source directory.
        
        Returns:
            Tuple of (moved_count, error_count)
        """
        moved = 0
        errors = 0
        
        if not self.video_source_dir.exists():
            return moved, errors
        
        video_files = list(self.video_source_dir.glob("*.webm"))
        for module_dir in self.video_source_dir.iterdir():
            if module_dir.is_dir():
                video_files.extend(module_dir.glob("*.webm"))

        for video in video_files:
            module = video.parent.name if video.parent != self.video_source_dir else "other"
            test_name = video.stem.replace("page@", "").replace(" - video", "")[:120]

            if self.move_video(video, test_name or "unknown", module=module):
                moved += 1
            else:
                errors += 1
        return moved, errors

    def get_execution_artifacts(self) -> dict:
        """Return moved artifact metadata for the current execution."""
        return self.execution_artifacts
    
    def get_screenshot_path(self, test_name: str, passed: bool = True) -> Optional[Path]:
        """Get the path where a screenshot would be saved."""
        dest_dir = self.pass_screenshot_dir if passed else self.fail_screenshot_dir
        new_filename = self._generate_filename(test_name, ".png")
        return dest_dir / new_filename
    
    def get_video_path(self, test_name: str, module: str = "other") -> Optional[Path]:
        """Get the path where a video would be saved."""
        module_dir = self.artifact_video_dir / module
        new_filename = self._generate_filename(test_name, ".webm")
        return module_dir / new_filename
