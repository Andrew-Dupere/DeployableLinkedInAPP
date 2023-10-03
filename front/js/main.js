
//even listener for each dropdown item
let dropdowns = document.getElementsByClassName('dropdown-item')

Array.from(dropdowns).forEach((dropdown) => { 
    dropdown.addEventListener('click', staticHandler)    
}); 


async function staticHandler(event){
    event.preventDefault()

    let terms = event.target.innerText 
    let info = await getStatAPI(terms)
    createTable(info,terms,'static-scrape-display')
    
}

//api call to the database query endpoint
async function getStatAPI(terms){
    let res = await fetch (`http://127.0.0.1:5000/api/db/${terms}`)    
    let rd = res.json()
    console.log(rd)

    return rd
}


//event listener for the linkedin scrape form
let form = document.getElementById('liform') 

form.addEventListener('submit',handler) 

async function handler(event){    

    event.preventDefault()    

    let terms = event.target.searchTerms.value  

    let info = await getAPI(terms)
    
    createTable(info,terms,'scrapeDisplay')
    
    event.target.searchTerms.value = '';
        
}

//api call to the linkedinscrape function
async function getAPI(terms){
    let res = await fetch (`http://127.0.0.1:5000/api/li/${terms}`)
    
    let rd = res.json()
    
    return rd
}


//create table function
function createTable(res,keywords,container){
    var tableContainer = document.getElementById(container)

    card = document.createElement('div')
    card.className = 'tableCard pt-4'

    let title = document.createElement('h3')
    title.innerHTML = `${keywords}`
    title.className = 'text-center'

    var table = document.createElement('table')
    table.className = 'w-100'
    var tbody = document.createElement('tbody')       
    
    var tableheader =      
                       `
                        <tr>
                            <th>Skill</th>
                            <th>Count</th>
                        </tr>`
    
    table.innerHTML += tableheader  

    var rowlist = []
    //pull apart the json response of each table row into an array within an array
    //sort the array in descending order based on the count
    //add the row to the table if the count (item[1]) value is > 1 

    for (const [key, value] of Object.entries(res)){
        rowlist.push([key,value])
    }
    rowlist.sort(function(a,b){return b[1]-(a[1])})

    for (const item of rowlist){
        if(item[1] > 1){
        var row = `<tr>
                    <td>${item[0]}</td>
                    <td>${item[1]}</td>       
                    </tr>`
            table.innerHTML += row
       }
    }
    card.append(title)
    table.append(tbody)
    card.append(table)
    tableContainer.prepend(card)
}

