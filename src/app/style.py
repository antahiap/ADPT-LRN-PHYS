import streamlit as st

css='''
<style>
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
    }

    /* Tooltip text */
    .tooltip .tooltiptext {
        font-size: 10px;
        visibility: hidden;
        width: 300px;
        background-color: black;
        color: #fff;
        text-align: center;
        padding: 5px;
        border-radius: 6px;

        bottom: 100%;
        left: 50%;
        margin-left: -150px; /* Use half of the width, to center the tooltip */
        
        /* Position the tooltip text - see examples below! */
        position: absolute;
        z-index: 1;
    }

    /* Show the tooltip text when you mouse over the tooltip container */
    .tooltip:hover .tooltiptext {
        visibility: visible;
    }

    /* Tooltip arrow */
    .tooltip .tooltiptext::after {
        content: " ";
        position: absolute;
        top: 100%; /* At the bottom of the tooltip */
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: black transparent transparent transparent;
    }
</style>
'''


gw, gh, txtw = 700, 500, 400
network_css =f'''

        <style type="text/css">

             #mynetwork {{
                 width: {gw}px;
                 height: {gh}px;
                 background-color: #ffffff;
                 border: 1px solid lightgray;
                 position: relative;
                 float: left;
             }}
             .column {{
              float: left;
              width: 50%;
            }}
            
            /* Clear floats after the columns */
            .row:after {{
              content: "";
              display: table;
              clear: both;
            }}
            #text{{
              height: {gw-200}px;
              width: {txtw}px;
              overflow: scroll;
            }}
             
        # </style>
'''