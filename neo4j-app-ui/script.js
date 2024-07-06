document.getElementById('search-button').addEventListener('click', () => {
    const query = document.getElementById('query-input').value;
  
    const config = {
      container_id: "viz",
      server_url: "bolt://localhost:7687",
      server_user: "neo4j",
      server_password: "password",
      labels: {
        "Character": {
          "caption": "name",
          "size": "pagerank",
          "community": "community"
        }
      },
      relationships: {
        "INTERACTS": {
          "thickness": "weight",
          "caption": false
        }
      },
      initial_cypher: query
    };
  
    const viz = new NeoVis.default(config);
    viz.render();
  });
  