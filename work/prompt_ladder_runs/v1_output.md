## ML Content-Refresh Prioritization

The project addressed a common SEO challenge: deciding which existing pages should be refreshed first. With a large content library, manually reviewing every page was slow, while prioritizing only by traffic decline overlooked pages with stronger recovery potential.

I developed a machine-learning prioritization system that ranked pages according to their expected value from a refresh. The model combined signals such as traffic and ranking trends, content age, search demand, engagement, conversion value, and previous refresh performance. Historical refresh outcomes were used to estimate the likely uplift for each page, while business rules accounted for effort, strategic importance, and prediction confidence.

The output was a ranked refresh queue rather than a simple “update/don’t update” classification. This made the system operationally useful: editors could focus limited capacity on pages with the highest expected return and understand the signals behind each recommendation.

In the measured evaluation period, the prioritized cohort achieved **[X%] greater organic uplift**, generated **[Y] additional visits/conversions**, and reduced manual analysis time by **[Z%]** compared with the previous selection process.

The project demonstrated how ML can turn content maintenance from a reactive, intuition-led workflow into a measurable allocation problem—helping teams invest editorial effort where it is most likely to produce results.