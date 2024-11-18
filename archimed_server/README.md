# Assumptions and Edge Cases in Fee Calculation Solution

## **Investment Date Validity**
It is assumed that the investment_date is valid and falls within the same calendar year as the fee calculation. The calculation considers only the fraction of the year after the investment date.

## **Fee Percentage**
The fee_percentage is provided as a whole number (e.g., 9.5), which is converted to a decimal (e.g., 0.095) for calculation.

## **End of Year**
The end of the year is fixed as December 31st of the same year as the investment_date.

## **Leap Year Consideration**
The solution handles both regular years (365 days) and leap years (366 days) by checking if the year is a leap year.

## **Yearly Fee Calculation**
The fee is calculated proportionally to the number of years investment made.

## **Input Data Validity**
The input data (investment amount, fee percentage, and investment date) is assumed to be valid and correctly formatted.

# **Edge Cases Handled in This System**

## **Multiple Investments**
- An investor can make multiple investments over time, each of which may have a different investment date, amount, and fee calculation based on the investment date and fee percentage.
- Each investment can generate separate bills for various fees (upfront, yearly, and membership fees) based on the investment date and the year in which the bill is created.

## **Bill Calculation for Multiple Investments**
### **Upfront Fees**
- If an investor pays upfront fees for one or more investments, the upfront fee will apply to each investment separately. This means the investor can have multiple upfront fee bills, one for each investment, covering the upfront fees for the corresponding investment.

### **Yearly Fees**
- For each investment, yearly fees will be calculated starting from the year after the upfront fee period ends. An investor with multiple investments will have multiple yearly fee bills. These bills will depend on the years_paid for each investment and the time the investment is active.

## **Bill Descriptions**
- Each bill generated for an investment will include details specific to that investment, such as the investment type, the years for which the fee applies, and the description explaining why the fee is being charged for that specific investment.
- The description will indicate the year of the investment, and whether it’s for an upfront fee, yearly fee, or membership fee. It will help in distinguishing between the various bills tied to different investments.

## **Handling Multiple Bills**
- Each bill will be linked to a specific investment, and it will be possible to retrieve and manage bills for each investment individually.
- For instance, if an investor has Investment 1 made in 2019 and Investment 2 made in 2022, they will have separate bills for each investment, even though they belong to the same investor. Both investments can have different fee structures, and the bills for each will be calculated based on the specific details of each investment.

## **Capital Call (Total Bills)**
- When calculating the capital call (total amount owed by the investor), the system will sum up all the bills across the investor's multiple investments.
- Each bill will be considered individually, and the total amount that the investor needs to pay will be the sum of all the bills from their investments.
- The due date for the capital call is set to 1 month from the date of generation.

## **Administrator Flexibility**
- Administrators will have the flexibility to modify or delete specific bills for individual investments as needed, allowing for a tailored billing process that can accommodate changes in payment structures, billing periods, or other adjustments specific to individual investments.
