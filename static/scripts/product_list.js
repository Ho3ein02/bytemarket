
// -------------- available filter -----------------
// let availableBtnElement = document.querySelector('.available-btn')
// let availableInputElement = document.querySelector('.available-input')
// availableBtnElement.addEventListener('click', function() {
//     availableBtnElement.classList.toggle('active')
// })



// ------------- price range filter -----------------
const rangevalue = document.querySelector(".slider-container .price-slider");
const rangeInputvalue = document.querySelectorAll(".range-input input");

// Set the price gap
let priceGap = 50;

// Adding event listners to price input elements
const priceInputvalue = document.querySelectorAll(".price-input input");
let maxPriceValue = priceInputvalue[0].getAttribute('max')
for (let i = 0; i < priceInputvalue.length; i++) {
    priceInputvalue[i].addEventListener("input", e => {

        // Parse min and max values of the range input
        let minp = parseInt(priceInputvalue[0].value);
        let maxp = parseInt(priceInputvalue[1].value);
        let diff = maxp - minp

        if (minp < 0) {
            priceInputvalue[0].value = 0;
            minp = 0;
        }

        // Validate the input values
        if (maxp > maxPriceValue) {
            priceInputvalue[1].value = Intl.NumberFormat().format(maxPriceValue);
            maxp = maxPriceValue;
        }

        if (minp > maxp - priceGap) {
            priceInputvalue[0].value = Intl.NumberFormat().format(maxp - priceGap);
            minp = maxp - priceGap;

            if (minp < 0) {
                priceInputvalue[0].value = 0;
                minp = 0;
            }
        }

        // Check if the price gap is met 
        // and max price is within the range
        if (diff >= priceGap && maxp <= rangeInputvalue[1].max) {
            if (e.target.className === "min-input") {
                rangeInputvalue[0].value = minp;
                let value1 = rangeInputvalue[0].max;
                rangevalue.style.left = `${(minp / value1) * 100}%`;
            }
            else {
                rangeInputvalue[1].value = maxp;
                let value2 = rangeInputvalue[1].max;
                rangevalue.style.right = 
                    `${100 - (maxp / value2) * 100}%`;
            }
        }
    });

    // Add event listeners to range input elements
    for (let i = 0; i < rangeInputvalue.length; i++) {
        rangeInputvalue[i].addEventListener("input", e => {
            let minVal = parseInt(rangeInputvalue[0].value);
            let maxVal = parseInt(rangeInputvalue[1].value);

            let diff = maxVal - minVal
            
            // Check if the price gap is exceeded
            if (diff < priceGap) {
            
                // Check if the input is the min range input
                if (e.target.className === "min-range") {
                    rangeInputvalue[0].value = maxVal - priceGap;
                }
                else {
                    rangeInputvalue[1].value = minVal + priceGap;
                }
            }
            else {
            
                // Update price inputs and range progress
                priceInputvalue[0].value = Intl.NumberFormat().format(minVal);
                priceInputvalue[1].value = Intl.NumberFormat().format(maxVal);
                rangevalue.style.right =
                    `${(minVal / rangeInputvalue[0].max) * 100}%`;
                rangevalue.style.left =
                    `${100 - (maxVal / rangeInputvalue[1].max) * 100}%`;
            }
        });
    }
}


