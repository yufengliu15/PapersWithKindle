import "../styles/global.css"
import AsciiArt from "../components/AsciiArt"
import AsciiGraph from "../components/AsciiGraph"

export default function Page() {
    return (
        <div className="content">
            <div className="header">
                <div className="header-title">
                    <h1>paperswithkindle</h1>
                </div>
                <div className="header-personal-website-link">
                    <h1><a href="https://yufengliu.tech" target="_blank">yufengliu.tech</a></h1>
                </div>
            </div>
            <AsciiArt></AsciiArt>
            <div className="email-signup">
                <div className="email-signup-text">
                    <p>
                    currently building...
                    </p>
                </div>                
            </div>
            <div className="ascii-art-bargraph-title">
                Number of Research Papers Per Category
            </div>
            <AsciiGraph></AsciiGraph>

        </div>
    )
}