document.getElementById('search-button').addEventListener('click', () => {
    const query = document.getElementById('query-input').value;  
      const config = {
      containerId: "viz",
      neo4j: {
          serverUrl: "bolt://localhost:7687",
          serverUser: "neo4j",
          serverPassword: "DurgaSahasra#2018",
      },
      labels: {
        Company :{
          label: "Company",
          size: 100,
          community: "Company",
          color: "#FF0000"  // Red color for Company nodes
        },
        Complaint:{
          label: "ComplaintId",
          community: "Complaint",
          color: "#00FF00"  // Green color for Complaint nodes
        }
          
      },
      relationships: {
        'AGAINST': {
                value: "type",
                label : "AGAINST",
                arrows: {
                    to: {enabled: true}
                }
            }
      },
      initialCypher: query
  };
  
    const viz = new NeoVis.default(config);
    viz.render();
  });
  