"""
使用例 (Usage Examples)

This file demonstrates how to use the Tokyo Weather API Client.
"""

from tokyo_weather import TokyoWeatherClient


def example_basic_usage():
    """基本的な使用例 (Basic usage example)"""
    print("=" * 60)
    print("例1: 基本的な使用 (Example 1: Basic Usage)")
    print("=" * 60)
    
    # APIキーを指定してクライアントを作成
    # Create client with API key (replace with your actual key)
    client = TokyoWeatherClient(api_key="your_api_key_here")
    
    # 整形された天気情報を取得
    # Get formatted weather information
    weather = client.get_formatted_weather()
    print(weather)


def example_different_units():
    """異なる単位での使用例 (Example with different units)"""
    print("\n" + "=" * 60)
    print("例2: 華氏での取得 (Example 2: Fahrenheit)")
    print("=" * 60)
    
    client = TokyoWeatherClient(api_key="your_api_key_here")
    
    # 華氏と英語で取得
    # Get in Fahrenheit and English
    weather = client.get_formatted_weather(units="imperial", lang="en")
    print(weather)


def example_raw_json():
    """生のJSONデータを取得する例 (Example getting raw JSON data)"""
    print("\n" + "=" * 60)
    print("例3: 生のJSONデータ (Example 3: Raw JSON Data)")
    print("=" * 60)
    
    client = TokyoWeatherClient(api_key="your_api_key_here")
    
    # 生のJSONデータを取得
    # Get raw JSON data
    data = client.get_current_weather()
    
    print(f"Location: {data.get('name', 'Tokyo')}")
    print(f"Weather: {data['weather'][0]['description']}")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Wind Speed: {data['wind']['speed']} m/s")


def example_with_env_variable():
    """環境変数を使用する例 (Example using environment variable)"""
    print("\n" + "=" * 60)
    print("例4: 環境変数からAPIキー取得 (Example 4: API Key from .env)")
    print("=" * 60)
    
    # .envファイルを作成して OPENWEATHER_API_KEY を設定しておく
    # Create .env file and set OPENWEATHER_API_KEY
    
    try:
        # APIキーを指定せずにクライアントを作成（環境変数から読み込む）
        # Create client without API key (reads from environment variable)
        client = TokyoWeatherClient()
        weather = client.get_formatted_weather()
        print(weather)
    except ValueError as e:
        print(f"Error: {e}")
        print("\n.envファイルに以下を設定してください:")
        print("OPENWEATHER_API_KEY=your_actual_api_key")


if __name__ == "__main__":
    print("東京天気APIクライアント 使用例")
    print("Tokyo Weather API Client - Usage Examples")
    print("\n注意: 実際のAPIキーを取得して使用してください")
    print("Note: Please obtain and use an actual API key from OpenWeatherMap")
    print("https://openweathermap.org/api\n")
    
    # 実際に実行する場合は、APIキーを設定して各関数のコメントを外してください
    # To actually run these examples, set your API key and uncomment the functions
    
    # example_basic_usage()
    # example_different_units()
    # example_raw_json()
    # example_with_env_variable()
    
    print("使用例のコードは examples.py を参照してください")
    print("See examples.py for usage example code")
