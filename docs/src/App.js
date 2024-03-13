import React, { useState } from "react";
import Project from "./Components/Project";
import Results from "./Components/Results";
import Collaborators from "./Components/Collaborators";
import OriginalCollaborators from "./Components/OriginalCollaborators";
import Repository from "./Components/Repository";

import "./App.css";

function App() {
  return (
    <div className="cointainer">
      <header className="bg-dark text-center text-white pt-3 pb-3">
        <h1>Monash Time-Series Forecasting Replication</h1>

        <h4>The University of Chicago</h4>
        <h4>Project of Data Science Tools for Finance</h4>

        <div id="buttons">
          <a href="#project" className="btn btn-secondary m-2">
            Project
          </a>
          <a href="#results" className="btn btn-secondary m-2">
            Results
          </a>
          <a href="#collaborators" className="btn btn-secondary m-2">
            Collaborators
          </a>
          <a href="#repository" className="btn btn-secondary m-2">
            Repository
          </a>
        </div>
      </header>

      <div className="cointainer mr-3 ml-3">
        <section id="project" className="bg-light p-3 mr-3 ml-3 pt-3">
          <Project />
        </section>
        <section id="results" className="p-3 mr-3 ml-3 pt-3">
          <Results />
        </section>
        <section id="repository" className="bg-light p-3 mr-3 ml-3 pt-3">
          <Repository />
        </section>
        <section id="collaborators" className="p-3 mr-3 ml-3 pt-3">
          <Collaborators />
        </section>
        <section id="original-collaborators" className="p-3 mr-3 ml-3 pt-3">
          <OriginalCollaborators />
        </section>
      </div>
    </div>
  );
}

export default App;
