# IMU FFT Analysis Tool

A professional Python tool for analyzing Inertial Measurement Unit (IMU) sensor data using Fast Fourier Transform (FFT) to identify frequency domain characteristics and signal patterns.

## Features

- **Comprehensive Analysis**: Supports 6-axis IMU data (3-axis accelerometer + 3-axis gyroscope)
- **Frequency Domain Analysis**: FFT-based spectral analysis with dominant frequency detection
- **Professional Visualizations**: Clean, publication-ready plots with customizable styling
- **Statistical Summaries**: Detailed statistical analysis and reporting
- **Modular Design**: Object-oriented architecture for easy integration and extension
- **Export Capabilities**: Save plots and analysis results to files

## Supported Hardware

- MPU9250 IMU sensors
- MPU6050 accelerometer/gyroscope sensors
- Any 6-axis IMU with similar data format

## Installation

### Prerequisites

```bash
pip install numpy pandas matplotlib
```

### Clone Repository

```bash
git clone https://github.com/yourusername/imu-fft-analysis.git
cd imu-fft-analysis
```

## Usage

### Basic Usage

```python
from imu_analyzer import IMUAnalyzer

# Initialize analyzer with your CSV file
analyzer = IMUAnalyzer("your_imu_data.csv")

# Load and analyze data
if analyzer.load_data():
    analyzer.calculate_sampling_params()
    analyzer.perform_fft_analysis()
    
    # Generate visualizations
    analyzer.create_comprehensive_plots(save_path="analysis_plots.png")
    
    # Generate comprehensive report
    summary_df = analyzer.generate_report()
```

### CSV Data Format

Your CSV file should contain the following columns:
- `time`: Timestamp in seconds
- `ax`, `ay`, `az`: Accelerometer data (g-force)
- `gx`, `gy`, `gz`: Gyroscope data (degrees/second)

Example:
```csv
time,ax,ay,az,gx,gy,gz
0.000,-0.012,0.098,0.987,0.23,-0.12,0.05
0.010,-0.015,0.095,0.989,0.21,-0.15,0.03
...
```

## Output

### Visualizations

The tool generates comprehensive plots, including:
- Time domain signals for accelerometer and gyroscope
- Frequency domain FFT analysis with **enhanced visual separation**
- Individual channel detailed analysis
- Professional styling with proper legends and labels

### Key Visualization Improvements:
- **Optimized FFT Axis Presentation**: 
  - FFT plots now start at **-0.2 Hz** (instead of 0 Hz) for cleaner visual separation
  - Creates a clear space between the 0 Hz label and the y-axis
  - Maintains all frequency information while improving readability
- **Consistent Axis Scaling**:
  - Combined FFT plots: X-axis from -0.2 Hz to Nyquist frequency (Fs/2)
  - Detailed plots: X-axis from -0.2 Hz to min(50, Fs/2)
- **Visual Buffer**: Negative space before 0 Hz ensures frequency labels don't touch axes

### Analysis Report

```
IMU DATA FFT ANALYSIS REPORT
============================================================

DATASET INFORMATION:
File: calibrated_mpu9250_data.csv
Shape: (1000, 7)
Duration: 10.000 seconds
Sampling rate: 100.0 Hz
Nyquist frequency: 50.0 Hz

DOMINANT FREQUENCY ANALYSIS:
----------------------------------------
Accel X (ax):
  Dominant frequency: 2.50 Hz
  Amplitude: 0.1234
  Signal range: -0.123 to 0.145 g
  Standard deviation: 0.045 g
...
```

### Summary Statistics Table

| Channel | Mean | Std | Range | Dom_Freq_Hz | Dom_Amplitude |
|---------|------|-----|-------|-------------|---------------|
| Accel X | 0.001 | 0.045 | 0.268 | 2.50 | 0.1234 |
| Accel Y | 0.012 | 0.038 | 0.234 | 1.75 | 0.0987 |
| ... | ... | ... | ... | ... | ... |

## Configuration

### Customization Options

```python
# Custom sensor configuration
analyzer.sensor_config['ax']['color'] = '#FF5733'  # Change plot colors
analyzer.sensor_config['ax']['unit'] = 'm/s²'      # Change units

# Plotting options
plt.rcParams['figure.dpi'] = 150  # Higher resolution plots
```

### Analysis Parameters

- **Frequency Resolution**: Automatically calculated based on sampling rate and data length
- **Nyquist Frequency**: Maximum detectable frequency (sampling_rate / 2)
- **DC Component Filtering**: Frequencies below 0.1 Hz are excluded from dominant frequency analysis

## Applications

- **Motion Analysis**: Identify movement patterns and frequencies
- **Vibration Monitoring**: Detect mechanical vibrations and resonances
- **Activity Recognition**: Analyze human activity patterns
- **Sensor Validation**: Verify sensor calibration and performance
- **Signal Processing Research**: Foundation for advanced IMU signal processing

## Technical Details

### Algorithm Overview

1. **Data Loading**: CSV parsing with automatic column mapping
2. **Sampling Analysis**: Automatic detection of sampling rate and parameters
3. **FFT Processing**: Efficient FFT computation using NumPy
4. **Statistical Analysis**: Comprehensive signal statistics calculation
5. **Visualization**: Professional matplotlib-based plotting

### Visualization Design Principles

The FFT plots follow professional data visualization standards:
1. **Axis Buffer Zones**: 
   - Implemented -0.2 Hz starting point for all frequency domain plots
   - Creates clean visual separation between labels and axes
   - Maintains full data integrity while improving presentation
   
2. **Intelligent Scaling**:
   - Combined plots show full spectrum up to Nyquist frequency
   - Detailed plots focus on 0-50Hz range (most relevant for motion analysis)
   - Automatic adjustment for different sampling rates

### Performance

- Handles datasets up to 1M+ samples efficiently
- Memory-optimized FFT processing
- Vectorized NumPy operations for fast computation
- Lightweight visualization rendering with optimized axis buffers

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{imu_fft_analyzer,
  title={IMU FFT Analysis Tool},
  author={Harshvardhan Wagare},
  year={2025},
  url={https://github.com/Codeharshw/imu-fft-analysis}
}
```

## Changelog

### v1.0.1
- **Visualization Enhancement**: 
- Improved FFT plot presentation with -0.2 Hz axis offset
- Added visual separation between 0 Hz label and plot axes
- Maintained all frequency information while enhancing readability

### v1.0.0
- Initial release with basic FFT analysis
- Professional plotting capabilities
- Comprehensive reporting system
- Support for 6-axis IMU data

## Support

For questions, bug reports, or feature requests, please open an issue on GitHub.

## Acknowledgments

- Built with NumPy, Pandas, and Matplotlib
- Tested with MPU9250 sensor data
