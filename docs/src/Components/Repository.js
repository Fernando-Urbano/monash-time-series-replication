import React from "react";

function Repository() {
  const githubUrl = "https://github.com/Fernando-Urbano/monash-time-series-replication";
  const githubMonashUrl = "https://github.com/Fernando-Urbano/monash-time-series-replication";

  return (
    <div className="container text-center">
      <h2 className="mb-4">Repository</h2>
      <p className="text-left">
        In our repository, we go in depth about the project details, how to replicate and update the results.
      </p>
      <p className="text-left">
        We invite you to start by reading the README file, which contains package dependencies, installation instructions, and a brief explanation of the project. 
      </p>
      <p className="text-left">
        Our dodo.py file serves as the main script for the project. It contains all the steps from data collection to model evaluation.
      </p>

      <a href={githubUrl} target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-lg active rounded text-center m-2 mb-4">
          Go to Our Repository
      </a>

      <p className="text-left">
        We base our work on the original paper and code from the authors. We also provide a link to their repository here:
      </p>

      <a href={githubMonashUrl} target="_blank" rel="noopener noreferrer" className="btn btn-secondary btn-lg active rounded text-center m-2">
          Go to Monash Time-Series Repository
      </a>

    </div>
  );
}

export default Repository;
