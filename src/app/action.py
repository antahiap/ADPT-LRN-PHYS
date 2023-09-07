node_onclick='''
        var network = drawGraph();

        // Function to display node properties
        function showNodeProperties(nodeId) {
            var node = nodes.get(nodeId);
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

        // Function to display edge properties
        function showEdgeProperties(edgeId) {
            var edge = edges.get(edgeId);
            var srcNode = nodes.get(edge.from);
            var dstNode =  nodes.get(edge.to);
            edgeTitle.textContent = srcNode.title + ' vs. ' + dstNode.title;

            console.log(edgeId);
            //nodeText.textContent = node.text;
        }

        // Add a click event listener to the graph
        network.on('click', function (params) {
            if (params.edges.length > 0) {
                var edgeId = params.edges[0];
                showEdgeProperties(edgeId);
            }
        });


'''