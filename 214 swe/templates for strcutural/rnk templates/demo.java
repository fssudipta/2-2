// Legacy Weather Service, which we cannot modify
class LegacyWeatherService {
    public String getWeatherData() {
        return "Legacy weather data";
    }
}

// Client Interface expected by the application
interface WeatherProvider {
    String fetchWeather();
}

// Application class that depends on the WeatherProvider interface
class WeatherApp {
    private WeatherProvider weatherProvider;

    public WeatherApp(WeatherProvider weatherProvider) {
        this.weatherProvider = weatherProvider;
    }

    public void displayWeather() {
        System.out.println(weatherProvider.fetchWeather());
    }
}

class WeatherServiceAdapter implements WeatherProvider{
    LegacyWeatherService legacyWeatherService;
    WeatherServiceAdapter(LegacyWeatherService legacyWeatherService){
        this.legacyWeatherService = legacyWeatherService;
    }
    public String fetchWeather(){
        return legacyWeatherService.getWeatherData();
    }
}

public class demo {
    public static void main(String[] args) {
        // Legacy service instance
        LegacyWeatherService legacyWeatherService = new LegacyWeatherService();
        WeatherServiceAdapter weatherServiceAdapter = new WeatherServiceAdapter(legacyWeatherService);
        WeatherApp app = new WeatherApp(weatherServiceAdapter);
        app.displayWeather(); // Output: Legacy weather data
    }
}