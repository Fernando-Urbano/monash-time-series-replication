import React from "react";
import data from "./test.json";
import Table from "./Table";
import MetricChart from "./MetricChart";

function Results() {
  const metrics = Object.keys(data);

  return (
    <div className="cointainer text-center">
      <h2 className="mt-3 mb-4">Results</h2>

      {metrics.map((metric) => (
        <section id={metric}>
          <h2 className="mt-4 mb-4 fw-normal text-decoration-underline">{metric}</h2>

          <div className="container border border-secondary p-3">
            <Table key={metric} data={data[metric]} />
          </div>
          <div className="container border border-secondary p-3">
            <MetricChart data={data[metric]} />
          </div>
        </section>
      ))}
    </div>
  );
}

export default Results;
