Airbnb Data Analysis
=====================

## **1. Business Understanding**

**Business Goal:**

To analyze how Airbnb saturation in specific neighborhoods impacts long-term housing affordability, providing insights for policymakers and urban planners.

**SMART Goal:**

To quantitatively measure the relationship between Airbnb listing density and long-term rental affordability in selected neighborhoods of Venice using Inside Airbnb data from the last 12 months, aiming to identify high-risk areas where short-term rental growth may threaten housing affordability by the end of the research period.

**SMART satisfaction breakdown:**

- **Specific:** Focuses on *Airbnb saturation* and *housing affordability risk* in *specific neighborhoods* of a given city.
- **Measurable:** Relationship will be measured using *Airbnb density metrics (listings per km²)* and *affordability proxies (average price, minimum nights, availability rate)*.
- **Achievable:** Data is directly available from Inside Airbnb; analysis tools (Python, pandas, etc.) are accessible.
- **Relevant:** Aligns with urban economic and data policy research objectives.
- **Time-bound:** Completion goal is *within research period*.

**Analytical Questions:**

*Descriptive AQs:*
1. What is the spatial distribution of Airbnb listings across neighborhoods?
2. What are the average nightly prices, availability rates, and minimum stay requirements in each neighborhood?
3. Which neighborhoods show the highest Airbnb density and revenue potential?

*Diagnostic AQs:*
1. Is there a correlation between Airbnb listing density and higher prices?
2. Do neighborhoods with more Airbnb activity have fewer long-term rental options (indicated by lower availability or higher minimum nights)?
3. Is Airbnb activity concentrated in the city center where visitors go, or spread evenly across Venice?

*Predictive AQs:*
1. Can we predict housing affordability risk (e.g., increasing price trends) based on Airbnb listing growth and density?
2. Which neighborhoods are most likely to experience further Airbnb saturation in the next 6 months?

*Prescriptive AQs:*
1. What regulations or policy interventions (e.g., limiting listings per host or minimum night stays) could stabilize affordability without harming the sharing economy?
2. Which neighborhoods should be prioritized for policy monitoring or intervention?

## **2. Data Understanding and Preparation**

- **Airbnb Listings**: Information about properties, including location, price, and availability.
- **Calendar data**: Daily availability and pricing information for listings.