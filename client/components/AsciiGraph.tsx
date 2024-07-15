'use client'
import Chartscii from "chartscii"
import papers from "../../papers.json"
import { useState, useEffect } from "react";

function windowSize(){
    const [windowSize, setWindowSize] = useState({
        width: undefined,
        height: undefined,
      });
    
      useEffect(() => {
        function handleResize() {
          setWindowSize({
            width: window.innerWidth,
            height: window.innerHeight,
          });
        }
    
        window.addEventListener('resize', handleResize);
        handleResize();
    
        return () => window.removeEventListener('resize', handleResize);
      }, []);
    
      return windowSize;
}

export default function AsciiGraph() {
    const size = windowSize()

    let data = formatJSON(papers)

    if (size.width < 915){
        const options = {
            width: size.width/38,
            height: data.length,
            valueLabels: true
        };
        var chart = new Chartscii(data, options).create();
        chart = chart.replace(/\u001b\[0m/g, '');
    } else {
        const options = {
            width: 50,
            height: data.length,
            valueLabels: true
        };
        var chart = new Chartscii(data, options).create();
        chart = chart.replace(/\u001b\[0m/g, '');
    }

    return (
        <div className="ascii-art-bargraph">
            <pre>
            {chart}
            </pre>
        </div>
    )
}

function formatJSON(papers){
    let data = []
    for (const category in papers){
        let JSONCat = {"label": "_", "value": 0}
        JSONCat.label = category
        JSONCat.value = papers[category].length
        data.push(JSONCat)
    }

    return data
}