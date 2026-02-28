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

class LegacyWeatherAdapter implements WeatherProvider {

    private LegacyWeatherService legacyService;

    public LegacyWeatherAdapter(LegacyWeatherService legacyService) {
        this.legacyService = legacyService;
    }

    public String fetchWeather() {
        // Translate the call
        return legacyService.getWeatherData();
    }
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

public class online_secA1 {
    public static void main(String[] args) {
        // Legacy service instance
        LegacyWeatherService legacyWeatherService = new LegacyWeatherService();
        // Wrap it with adapter
        WeatherProvider adapter = new LegacyWeatherAdapter(legacyWeatherService);
        WeatherApp app = new WeatherApp(adapter);
        app.displayWeather(); // Output: Legacy weather data
    }
}