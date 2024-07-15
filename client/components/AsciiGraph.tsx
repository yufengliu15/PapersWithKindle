'use client'
import Chartscii from "chartscii"
import papers from "../../papers.json"

export default function AsciiGraph() {
    let data = [{"label": "Machine Learning", "value": 100}, {"label": "AI", "value": 83}, {"label": "HCI", "value": 70}]
    
    data = formatJSON(papers)
    console.log(papers["Artificial Intelligence"].length)
    const options = {
        width: 50,
        height: data.length,
        orientation: "horizontal",
        valueLabels: true
    };
    var chart = new Chartscii(data, options).create();
    chart = chart.replace(/\u001b\[0m/g, '');
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
        let JSONCat = {"label": "idk", "value": 0}
        JSONCat.label = category
        JSONCat.value = papers[category].length
        data.push(JSONCat)
    }

    return data
}