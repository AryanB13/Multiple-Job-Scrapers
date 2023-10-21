const unirest = require("unirest")
const ObjectsToCsv = require('objects-to-csv');
const cheerio = require("cheerio")

const getJobData = async () => {
    try {
        let range = 50
        let pageNum = 0;
        for (let i = 0; i < range; i++) {
            let url = `https://in.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software&location=India&start=${pageNum}`
            pageNum += 25;
            let response = await unirest.get(url).headers({ "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36" })
            const $ = cheerio.load(response.body)

            let jobs_data = []
            $(".job-search-card").each((i, el) => {

                jobs_data.push({
                    title: $(el).find(".base-search-card__title").text()?.trim(),
                    company: $(el).find("h4.base-search-card__subtitle").text()?.trim(),
                    link: $(el).find("a.base-card__full-link").attr("href")?.trim(),
                    location: $(el).find(".job-search-card__location").text()?.trim(),
                    date: $(el).find(".job-search-card__listdate").text()?.trim(),
                })
            })
            const csv = new ObjectsToCsv(jobs_data)
            csv.toDisk('./linkedInJobs2.csv', { append: true })
        }
    }
    catch (e) {
        console.log(e)
    }
}

getJobData()