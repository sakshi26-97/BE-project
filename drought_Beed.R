library(dplyr)
library(tseries)
library(MASS)
data <- read.csv('SPI_Beed.csv', header = T)
#attach(data)

# To create time-series object
#spiarima <- ts(data$SPI ,frequency=12, start=c(1990,1))
#ts <- ts(data$SPI, start=c(2010,1), end=c(2017,12), frequency=12)
#plot(spiarima)
#title("time series plot lndata")
#dim(as.matrix(spiarima))


# Plot and convert to ln format
#data$SPI[1:1393] + 1
#min(data$SPI)
lnSPI = log(data$SPI[1058:1357]+1-min(data$SPI))  #translate and then transform
#View(lnSPI)
lnSP=1.946
# ACF, PACF and Dickey-Fuller Test
acf(lnSPI, lag.max=20, na.action = na.pass)
pacf(lnSPI, lag.max=20, na.action = na.pass)
# To check whether the dataset is stationary or not
adf.test(as.numeric(na.omit(lnSPI)))
#PP.test(ts)
#kpss.test(ts)


# To create time-series object
spiarima <- ts(lnSPI,frequency=12, start=c(2000,1))
#ts <- ts(data$SPI, start=c(2010,1), end=c(2017,12), frequency=12)
plot(spiarima)
title("time series plot lndata")
dim(as.matrix(spiarima))

components <- decompose(spiarima)
components
plot(components)


#Developing SARIMA model and Analysis of Model
library(forecast)
fitlnspi = auto.arima(spiarima, trace = TRUE, test = "kpss", ic="bic")
fitlnspi
summary(fitlnspi)
confint(fitlnspi)
x=exp(lnSP)



# Forecasted Values From ARIMA
arima_model.forecast = forecast(fitlnspi, h=35)
arima_model.forecast
plot(arima_model.forecast)

# the data needs to be converted back into its original format by calculating the exponent of the log predictions.
#These predictions are then compared against the test data to identify
forecastedvaluesextracted=as.numeric(arima_model.forecast$mean)
forecastedvaluesextracted
finalforecastvalues=exp(forecastedvaluesextracted) - 1 + min(data$SPI)
finalforecastvalues


# the forecasted values have been calculated
#compare this against the test data to forecast the percentage error:
# Percentage Error
df<-data.frame(data$SPI[1118:1392],finalforecastvalues)
col_headings<-c("Actual SPI","Forecasted SPI")
names(df)<-col_headings
#attach(df)


percentage_error=((df$'Actual SPI'-df$'Forecasted SPI')/(df$'Actual SPI'))
percentage_error

mean(percentage_error)

percentage_error=data.frame(abs(percentage_error))
accuracy=data.frame(percentage_error[percentage_error$abs.percentage_error. < 0.1,])
frequency=as.data.frame(table(accuracy))
sum(frequency$Freq)/(275/x)

#Residuals Diagonostics
plot.ts(fitlnspi$residuals)
Box.test(fitlnspi$residuals, lag=5, type = "Ljung-Box")
Box.test(fitlnspi$residuals, lag=10, type = "Ljung-Box")
Box.test(fitlnspi$residuals, lag=15, type = "Ljung-Box")
#acf(arima_model$residuals, lag.max = 24, main="ACF of the model")

Box.test(fitlnspi$residuals, lag=20, type = "Ljung-Box")
#library(tseries)
#jarque.bera.test(arima_model$residuals)


x = array(as.numeric(finalforecastvalues), dim=60)
#x[60]
#print(typeof(x))

for(i in 1:60)
{
  if (x[i]<0 && x[i]>-0.99)
    print("Mild Drought")
  else if(x[i]<-1 && x[i]>-1.49)
    print("Moderate Drought")
  else if(x[i]<-1.5 && x[i]>-1.99)
    print("Severe Drought")
  else if(x[i]<-2)
    print("Extreme Drought")
  else
    print("No Drought")
}
plot(finalforecastvalues, xlab = "Years", ylab = "SPI")

library(TSPred)
plotarimapred(data.test, finalforecastvalues, xlim = c(2016,2020), range.percent=0.05)


library(openxlsx)
library(writexl)
data <- data.frame(matrix(finalforecastvalues,nrow=35,ncol=1))
write_xlsx(data, "F:/mydata.xlsx")
