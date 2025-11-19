"""
東京天気APIクライアントのテスト
Tests for Tokyo Weather API Client
"""

import unittest
from unittest.mock import patch, Mock
import requests
from tokyo_weather import TokyoWeatherClient


class TestTokyoWeatherClient(unittest.TestCase):
    """TokyoWeatherClientのテストケース (Test cases for TokyoWeatherClient)"""
    
    def setUp(self):
        """各テストの前に実行される (Run before each test)"""
        self.api_key = "test_api_key_12345"
        self.client = TokyoWeatherClient(api_key=self.api_key)
    
    def test_init_with_api_key(self):
        """APIキーでの初期化をテスト (Test initialization with API key)"""
        client = TokyoWeatherClient(api_key="test_key")
        self.assertEqual(client.api_key, "test_key")
    
    def test_init_without_api_key_raises_error(self):
        """APIキーなしの初期化でエラーが発生することをテスト"""
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError) as context:
                TokyoWeatherClient()
            self.assertIn("APIキーが設定されていません", str(context.exception))
    
    def test_tokyo_coordinates(self):
        """東京の座標が正しく設定されていることをテスト"""
        self.assertAlmostEqual(TokyoWeatherClient.TOKYO_LAT, 35.6762, places=4)
        self.assertAlmostEqual(TokyoWeatherClient.TOKYO_LON, 139.6503, places=4)
    
    @patch('tokyo_weather.requests.get')
    def test_get_current_weather_success(self, mock_get):
        """天気情報の取得が成功することをテスト"""
        # モックレスポンスを設定 (Set up mock response)
        mock_response = Mock()
        mock_response.json.return_value = {
            'weather': [{'description': '晴れ'}],
            'main': {
                'temp': 20.5,
                'feels_like': 19.0,
                'temp_min': 18.0,
                'temp_max': 22.0,
                'humidity': 60
            },
            'wind': {'speed': 3.5}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # テスト実行 (Execute test)
        result = self.client.get_current_weather()
        
        # 検証 (Verify)
        self.assertIn('weather', result)
        self.assertIn('main', result)
        self.assertEqual(result['weather'][0]['description'], '晴れ')
        self.assertEqual(result['main']['temp'], 20.5)
        
        # APIが正しいパラメータで呼ばれたことを確認
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertEqual(call_args[1]['params']['lat'], TokyoWeatherClient.TOKYO_LAT)
        self.assertEqual(call_args[1]['params']['lon'], TokyoWeatherClient.TOKYO_LON)
        self.assertEqual(call_args[1]['params']['appid'], self.api_key)
    
    @patch('tokyo_weather.requests.get')
    def test_get_current_weather_with_units(self, mock_get):
        """異なる単位での天気情報取得をテスト"""
        mock_response = Mock()
        mock_response.json.return_value = {'weather': [{}], 'main': {}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # 華氏でテスト (Test with Fahrenheit)
        self.client.get_current_weather(units="imperial", lang="en")
        
        call_args = mock_get.call_args
        self.assertEqual(call_args[1]['params']['units'], "imperial")
        self.assertEqual(call_args[1]['params']['lang'], "en")
    
    @patch('tokyo_weather.requests.get')
    def test_get_current_weather_request_exception(self, mock_get):
        """API呼び出し失敗時の例外処理をテスト"""
        # リクエスト例外を発生させる (Raise request exception)
        mock_get.side_effect = requests.RequestException("Network error")
        
        # 例外が発生することを確認 (Verify exception is raised)
        with self.assertRaises(requests.RequestException) as context:
            self.client.get_current_weather()
        self.assertIn("天気情報の取得に失敗しました", str(context.exception))
    
    @patch('tokyo_weather.requests.get')
    def test_get_formatted_weather(self, mock_get):
        """整形された天気情報の取得をテスト"""
        # モックレスポンスを設定
        mock_response = Mock()
        mock_response.json.return_value = {
            'weather': [{'description': '晴天'}],
            'main': {
                'temp': 25.0,
                'feels_like': 24.0,
                'temp_min': 22.0,
                'temp_max': 27.0,
                'humidity': 55
            },
            'wind': {'speed': 2.5}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # テスト実行
        result = self.client.get_formatted_weather()
        
        # 検証 - 各要素が含まれていることを確認
        self.assertIn('東京の天気情報', result)
        self.assertIn('晴天', result)
        self.assertIn('25.0', result)
        self.assertIn('°C', result)
        self.assertIn('55%', result)
    
    @patch('tokyo_weather.requests.get')
    def test_get_formatted_weather_imperial(self, mock_get):
        """華氏での整形された天気情報をテスト"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'weather': [{'description': 'Clear sky'}],
            'main': {
                'temp': 77.0,
                'feels_like': 75.0,
                'temp_min': 72.0,
                'temp_max': 81.0,
                'humidity': 55
            },
            'wind': {'speed': 5.5}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = self.client.get_formatted_weather(units="imperial")
        
        # 華氏記号が含まれていることを確認
        self.assertIn('°F', result)
        self.assertIn('77.0', result)


if __name__ == '__main__':
    unittest.main()
