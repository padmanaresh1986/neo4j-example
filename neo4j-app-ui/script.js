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
          
      },
      relationships: {
          
      },
      initialCypher: query
  };
  
    const viz = new NeoVis.default(config);
    viz.render();
  });
  