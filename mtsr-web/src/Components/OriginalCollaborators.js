import React from "react";
import "./Styles/Collaborators.css";

// images
import photo1 from "./Images/person1_monash.jpg";
import photo2 from "./Images/person2_monash.jpg";
import photo3 from "./Images/person3_monash.jpg";
import photo4 from "./Images/person4_monash.jpg";
import photo5 from "./Images/person5_monash.jpg";

function OriginalCollaborators() {
  const collaborators = [
    { image: photo1, name: "Rakshitha Godahewa", email: "" },
    { image: photo2, name: "Christoph Bergmeir", email: "" },
    { image: photo3, name: "Geoff Webb", email: "" },
    { image: photo4, name: "Rob Hyndman", email: "" },
    { image: photo5, name: "Pablo Montero-Manso", email: "" },
  ];

  return (
    <div className="container">
      <div className="mt-3 text-center mb-5">
        <h2 className="mb-4">Monash Time-Series Archive Collaborators</h2>
        <p>
          The creators of the original project are a group of time series researchers from Monash University and University of Sydney:
        </p>
      </div>

      <div class="row text-center">
        {collaborators.slice(0, 3).map((collaborator) => (
          <div className="col-12 text-center col-md-4 col-sm-6 mb-4">
            <img
              src={collaborator.image}
              alt={collaborator.name}
              className="rounded image-fixed-size"
            />
            <p className="mt-2">{collaborator.name}</p>
            <p>{collaborator.email}</p>
          </div>
        ))}
      </div>

      <div class="row text-center mb-4">
        <div className="col-md-2"></div>
        {collaborators.slice(3, 5).map((collaborator) => (
          <div className="col-12 text-center col-md-4 col-sm-6 mb-4">
            <img
              src={collaborator.image}
              alt={collaborator.name}
              className="rounded image-fixed-size"
            />
            <p className="mt-2">{collaborator.name}</p>
            <p>{collaborator.email}</p>
          </div>
        ))}
        <div className="col-md-2"></div>
      </div>
      
    </div>
  );
}

export default OriginalCollaborators;
