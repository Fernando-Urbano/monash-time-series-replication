import React from 'react';

function Project() {
  return (
    <div className="container">
      <h2 className="text-center mb-4">Project</h2>
      <p>
        Our project is a replication of the Monash Time Series Forecasting Article and Archive. 
      </p>
      <p>
        The Monash Archive is an essential asset to time series researchers as it provides a comprehensive benchmark time series forecasting archive to evaluate the performance of new global and multivariate forecasting algorithms.
      </p>
      <p>
        Specifically, as researchers branch further and further into the machine learning space, the Monash Archive allows them to test the generalized performance of their models against well-tested benchmark models, which is beneficial in addressing the questions of model overfitting and performance. The archive contains datasets spanning multiple domains (industries) as well as 13 forecasting models, 6 of which are canonical univariate models, and 7 of which are global models that have shown positive results in recent years. In the following sections we provide a brief description of each of the datasets used, as well as an overview of the important aspects of the models used. 
      </p>
      <p>
        In our replication, we constructed a repository that automates the entire process of data download to error metric forecasting calculation for 7 out of the 13 models, evaluating 30 datasets from the Monash Archive. Furthermore, we generate a report that provides a comprehensive overview of the performance of the models, discussion of the results, our sucesses and challenges.
      </p>
      <p>
        We invite you to check and clone the repository. You will be able to run the models, update the results and generate a full report with information about the datasets and forecasting errors.
        You can read more about in the "Repository" section!
      </p>
      <p>
        In the next section, we provide a brief overview of forecasting error metric results for different models and datasets.
      </p>
    </div>
  );
}

export default Project;