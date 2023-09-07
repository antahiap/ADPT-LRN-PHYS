node_onclick='''
        var network = drawGraph();

        // Function to display node properties
        function showNodeProperties(nodeId) {
            var node = nodes.get(nodeId);
            var propertiesDiv = document.getElementById('text');
            nodeTitle.textContent = node.ids + ' ' + node.title;
            nodeText.textContent = node.text;
        }

        // Add a click event listener to the graph
        network.on('click', function (params) {
            if (params.nodes.length > 0) {
                var nodeId = params.nodes[0];
                showNodeProperties(nodeId);
            }
        });
'''