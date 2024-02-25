from typing import Union, Callable, Optional
import requests
import os
import pandas as pd

'''
Generic class for obtaining data from an online source.
Is initialized with:
    - The url for the source
    - The path where the raw resource should be saved
    - The path where the processed file should be saved
    - The 'parse function' which should be used to process the raw file.
'''
class DataSource:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    def __init__(self, 
                 url: Union[str, list[str]], 
                 parse: Callable[[str], pd.DataFrame],
                 raw_path: Optional[str] = None,
                 processed_path: Optional[str] = None,
                 encoding='utf-8'):
        self.url = url
        self.raw_path = raw_path
        self.processed_path = processed_path
        self.encoding = encoding

        self._parse = parse
        self._raw_content = ''
        self._df = None
        self._txt = None

    def _request_raw(self):
        if isinstance(self.url, str):
            self.url = [self.url]
        for url in self.url:
            response = requests.get(url, headers=DataSource.headers)
            if response.status_code != 200:
                print(f"{self.__class__}: Failed to retrieve the HTTP response. Status code: {response.status_code}")
                return None
            self._raw_content += response.content.decode(self.encoding)

    def _save_raw(self):
        if not self.raw_path:
            return
        content = self.raw_content
        with open(self.raw_path, 'w', encoding=self.encoding) as f:
            f.write(content)

    @property
    def raw_content(self):
        if self._raw_content:
            return self._raw_content
        if self.raw_path and os.path.isfile(self.raw_path):
            with open(self.raw_path, 'r', encoding=self.encoding) as f:
                self._raw_content = f.read()
        else:
            self._request_raw()
            self._save_raw()
        return self._raw_content

    def _save_csv(self):
        if not self.processed_path:
            return
        try:
            self.df.to_csv(self.processed_path)
        except PermissionError:
            print(f"Unable to save {self.processed_path}. Is it being used by another program? (Excel?)")

    @property
    def df(self):
        if self._df is not None:
            return self._df
        if self.processed_path and os.path.isfile(self.processed_path):
            self._df = pd.read_csv(self.processed_path)
        else:
            self._df = self._parse(self.raw_content)
            self._save_csv()
        return self._df
    
    def _save_txt(self):
        if not self.processed_path:
            return
        content = self.txt
        with open(self.processed_path, 'w', encoding=self.encoding) as f:
            f.write(content)
    
    @property
    def txt(self):
        if self._txt is not None:
            return self._txt
        if self.processed_path and os.path.isfile(self.processed_path):
            with open(self.processed_path, 'r', encoding=self.encoding) as f:
                self._txt = f.read()
        else:
            self._txt = self._parse(self.raw_content)
            self._save_txt()
        return self._txt

