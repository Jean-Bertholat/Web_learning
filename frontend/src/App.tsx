import React from 'react';
import './App.css';
import { RegionInfoDisplay } from './components/region_info_display';
import { WeatherDisplay } from './components/weather_display';


function App() {
  return (
      <div className="App">
        <header className="App-header">
          <h1>Weather App</h1>
        </header>
        <main>
          <WeatherDisplay region="Paris" />
          <RegionInfoDisplay regionId={10} />
        </main>
      </div>
  );
}

export default App;
