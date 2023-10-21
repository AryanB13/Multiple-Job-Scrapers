const unirest = require("unirest")
const ObjectsToCsv = require('objects-to-csv');
const cheerio = require("cheerio")



async function getJobData() {
    url = `https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&per_page=15&searchTerm=software%20developer&oppstatus=recent&location=Bengaluru&page=1`;
    let range = 0;
    let jobs_data=[]
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        range = data.data.last_page;
        //console.log(data.data);

        for (let i = 0; i < 10; i++) {
            jobs_data.push({
                title: data.data.data[i].title,
                company: data.data.data[i].organisation.name,
                link: data.data.data[i].seo_url,
                location: data.data.data[i].jobDetail.locations,
                date: data.data.data[i].regnRequirements.remain_days,
            })
        }
        console.log(jobs_data);

        for (let j = 2; j < range; j++) {
            const url1 = `https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&per_page=15&searchTerm=software%20developer&oppstatus=recent&location=Bengaluru&page=${j}`;

            const response = await fetch(url1);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            for (let i = 0; i < 10; i++) {
                jobs_data.push({
                    title: data.data.data[i].title,
                    company: data.data.data[i].organisation.name,
                    link: data.data.data[i].seo_url,
                    location: data.data.data[i].jobDetail.locations,
                    date: data.data.data[i].regnRequirements.remain_days,
                })
            }
        }


        const csv = new ObjectsToCsv(jobs_data)
        csv.toDisk('./UnstopJobs2.csv', { append: true })

    }
    catch (error) {
        console.error("An error occurred:", error);
    }
}

getJobData()