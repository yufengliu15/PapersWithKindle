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

            <div className="references-section">
                <div className="references-section-title">
                    <p>References</p>
                </div>
                <div className="references-section-text">
                    <p>Papers were scraped from this website maintained by Jeff Huang:</p>
                    <a href="https://jeffhuang.com/best_paper_awards/conferences.html" target="_blank">https://jeffhuang.com/best_paper_awards/conferences.html</a>
                </div>
            </div>

            <br></br>
            <br></br>
            <br></br>
            <br></br>

        </div>
    )
}