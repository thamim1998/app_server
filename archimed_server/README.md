# Description about the every segment of this system

## **Uniqueness of Entities**

### **Investor**
- **Investors** are unique in the system. Each investor can have multiple investments, but each investor record is singular and cannot be duplicated. 
- The system ensures that no duplicate **investor** data exists.

### **Investment**
- Each **investment** is also unique. An **investment** record is tied to a specific **investor** and contains investment-specific details, such as the **investment_date**, **investment_amount**, **fee_percentage**,**upfromt_fee**, **yearly_fee** and the corresponding **membership_fee**.
- The system allows an investor to make multiple investments, but each **investment** record is distinct and cannot be duplicated.

### **Bills**
- **Bills** are generated for each **investment** based on the relevant fees. Each bill has unique characteristics such as **bill_type** (upfront, yearly, membership) and **bill_year**, ensuring no duplication of bills for the same **investment** and year.
- A **bill** is associated with an **investment** and can have details about the fee type, amount, description, and due date.
- Each **bill** has a unique identifier that prevents the same bill from being generated multiple times for the same **investment**.

### **Active Member** ###
- An **active member** is an **investor** who is currently participating in the program and has been explicitly marked as active by the **administrator**.

### **Membership** ###
 - This fee is calculated annually and is separate from investment-specific fees (like **upfront fees** or **yearly fees** for individual investments).
 - No membership fee bills are generated for **inactive investors**.
 - A **membership fee** is waived for **investors** who have invested more than **50,000 EUR**.
 - If an investor becomes active in a year later than their **initial investment**, **membership fees are calculated starting from the year they became active** (not their investment year). 

### **Capital Call**
- **Capital Calls** represent the total amount owed by an investor across all their investments, summed from the various **bills**. 
- The **capital_call** is a unique total for an investor and is generated once, based on all outstanding **bills**. 
- The system ensures that the **capital call** for an investor is unique, meaning each **capital call** can only be generated once for an investor for each period.

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
- Administrators will have the flexibility to modify or delete specific bills for individual investments as needed, allowing for a tailored billing process that can accommodate changes in status, billing periods, or other adjustments specific to individual investments.
