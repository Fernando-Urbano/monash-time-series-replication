import React from "react";
import "./Styles/Collaborators.css";

// images
import photo1 from "./Images/person1.jpg";
import photo2 from "./Images/person2.jpg";
import photo3 from "./Images/person3.jpg";
import photo4 from "./Images/person4.jpg";
import photo5 from "./Images/person5.jpg";

function Collaborators() {
  const collaborators = [
    { image: photo1, name: "Fernando Urbano", email: "fernandourbano@uchicago.edu" },
    { image: photo2, name: "Jeremy Bejarano", email: "jbejarano@uchicago.edu" },
    { image: photo3, name: "Aben Carrington", email: "acarrington@uchicago.edu" },
    { image: photo4, name: "Shrey Jain", email: "shreyjain@uchicago.edu" },
    { image: photo5, name: "Mukund Maheshwari", email: "mukundmaheshwari@uchicago.edu" },
  ];

  return (
    <div className="container">
      <div className="mt-3 text-center mb-5">
        <h2 className="mb-4">Replication Collaborators</h2>
        <p>
          This replication project was developed by a team of students from the University of Chicago with the help of Professor Jeremy Bejarano.
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

export default Collaborators;
