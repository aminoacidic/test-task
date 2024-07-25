import os
from collections import defaultdict
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def categorize_files_by_type(folder_path, min_size=None, max_size=None, last_modified_after=None, last_modified_before=None):
    if not os.path.isdir(folder_path):
        raise ValueError(f"The provided path {folder_path} is not a valid directory.")
    
    file_dict = defaultdict(list)
    
    def scan_directory(path):
        try:
            entries = os.listdir(path)
        except PermissionError:
            logging.warning(f"Permission denied: {path}")
            return

        for entry in entries:
            entry_path = os.path.join(path, entry)
            if os.path.isfile(entry_path):
                file_ext = os.path.splitext(entry)[1] if os.path.splitext(entry)[1] else ''
                file_stat = os.stat(entry_path)

                # Apply optional filters
                if min_size is not None and file_stat.st_size < min_size:
                    continue
                if max_size is not None and file_stat.st_size > max_size:
                    continue
                if last_modified_after is not None and file_stat.st_mtime < last_modified_after.timestamp():
                    continue
                if last_modified_before is not None and file_stat.st_mtime > last_modified_before.timestamp():
                    continue

                file_dict[file_ext].append(os.path.abspath(entry_path))
            elif os.path.isdir(entry_path):
                scan_directory(entry_path)

    scan_directory(folder_path)
    
    logging.info(f"Categorization complete. Processed {len(file_dict)} file types.")
    return dict(file_dict)

# Example usage
folder_path = '/Users/aminabekbayeva/Downloads/TestTask'
if os.path.isdir(folder_path):
    result = categorize_files_by_type(folder_path)

    # Print the result
    for ext, files in result.items():
        print(f"Extension: '{ext}'")
        for file in files:
            print(f"  - {file}")
else:
    print(f"The provided path {folder_path} does not exist or is not a valid directory.")

# Tests using unittest
import unittest
from datetime import datetime, timedelta

class TestCategorizeFilesByType(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        os.makedirs('test_dir/subdir', exist_ok=True)
        with open('test_dir/file1.txt', 'w') as f:
            f.write('Hello World')
        with open('test_dir/subdir/file2.jpg', 'w') as f:
            f.write('Hello World')
        with open('test_dir/file3', 'w') as f:
            f.write('Hello World')
    
    def tearDown(self):
        # Clean up the temporary directory structure after tests
        import shutil
        shutil.rmtree('test_dir')

    def test_categorize_files_by_type(self):
        result = categorize_files_by_type('test_dir')
        expected = {
            '.txt': [os.path.abspath('test_dir/file1.txt')],
            '.jpg': [os.path.abspath('test_dir/subdir/file2.jpg')],
            '': [os.path.abspath('test_dir/file3')]
        }
        self.assertEqual(result, expected)

    def test_filters(self):
        result = categorize_files_by_type('test_dir', min_size=20)
        self.assertEqual(result, {})
        
        future_date = datetime.now() + timedelta(days=1)
        result = categorize_files_by_type('test_dir', last_modified_before=future_date)
        self.assertIn(os.path.abspath('test_dir/file1.txt'), result['.txt'])

if __name__ == '__main__':
    unittest.main()

# Print extension type and directory as requested
if os.path.isdir(folder_path):
    result = categorize_files_by_type(folder_path)

    # Print the result
    for ext, files in result.items():
        print(f"Extension: '{ext}'")
        for file in files:
            print(f"  - {file}")
else:
    print(f"The provided path {folder_path} does not exist or is not a valid directory.")
