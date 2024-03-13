import React from "react";

function Table({ data }) {
  const models = Object.keys(data);

  let datasetsNamesSet = new Set();

  models.forEach(model => {
    Object.keys(data[model]).forEach(dataset => {
      datasetsNamesSet.add(dataset);
    });
  });

  const datasetsNames = Array.from(datasetsNamesSet); 

  // Utility function to format the value
  const formatValue = (value) => {
    // Check if value exists and is not null
    if (value == null) { // This checks for both `undefined` and `null`
      return '-';
    }
    if (value > 999) {
      return value.toExponential(1); // Converts to scientific notation
    }
    return value;
  };

  return (
    <table className="table table-bordered">
      <thead className="thead-dark">
        <tr>

          <th scope="col">Dataset</th>

          {models.map((model) => (
            <th scope="col">{model}</th>
          ))}

        </tr>
      </thead>
      <tbody>

          {datasetsNames.map((datasetName) => (
            <tr>
              <th scope="row">{datasetName}</th>
              {models.map((model, modelIndex) => (
              <td key={modelIndex}>
                {formatValue(data[model][datasetName])}
              </td>
            ))}
            </tr>
          ))}

      </tbody>
    </table>
  );
}

export default Table;
