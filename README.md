# Bosch washing machine power usage

## Washing machine

- 9kg capacity
- 1400rpm spin speed
- Serie 8
- E-Nr: WAW28420AU/24

## Results

![Box and whisker](plot_data.png)

## Conclusions

- Power usage clearly depends on temperature.  A useful rule of thumb is power usage is $0.02\times(T - 20)$ kWh.  Viz, very small for cold washes, 0.2kWh for 30degC, 0.4kWh for 40degC, and 0.8kWh for 60degC.  Probably, the cold-water temperature is about 20degC here in Australia.  Heating water is the dominant energy requirement.
- Within one cycle type and temperature, there is substantial variation.  Anecdotally, I suspect the variation depends on type and amount of clothes to be washed.  In practice, it's difficult to check this because I don't wear exactly the same clothes all the time!
- Mix speed at 40degC has a statistically higher power usage than Mix eco at 40degC.
  - Mix speed: mean = 0.411 kWh, SD = 0.091, n = 30
  - Mix eco:   mean = 0.335 kWh, SD = 0.068, n = 22
  - Difference in means (speed - eco) = 0.077 kWh
  - 95% CI for difference = [0.032, 0.121] kWh
  - Welch t-test: t = 3.475, df = 50.0, p = 0.001066
- Another example of "speed" vs "eco", washing the same set of towels under nominally identical conditions costs 0.53 kWh on "speed" and only 0.36 kWh on "eco".


