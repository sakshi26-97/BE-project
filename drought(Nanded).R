library(dplyr)
library(tseries)
data <- read.csv('SPI_Nanded.csv', header = T)
#View(data)
#data <- subset(data,select=c(2))
#data = log(data)
#data$SPI[is.na(data$SPI)] <- 0

# To create time-series object
ts <- ts(data$SPI6,frequency=12, start=c(2005,1))
#ts <- ts(data$SPI, start=c(2010,1), end=c(2017,12), frequency=12)
plot(ts)
dim(as.matrix(ts))

# To check whether the dataset is stationary or not
adf.test(ts)
#PP.test(ts)
#kpss.test(ts)


#Training and Testing dataset

data.train = window(ts, start = c(2005,1), end=c(2015,12))
plot(data.train)
dim(as.matrix(data.train))
data.test = window(ts, start = c(2016,1))
plot(data.test)
dim(as.matrix(data.test))

#Developing SARIMA model and Analysis of Model
library(forecast)
arima_model = auto.arima(data.train, trace = TRUE, test = "kpss", ic="aic")
summary(arima_model)
confint(arima_model)

#Residuals Diagonostics
plot.ts(arima_model$residuals)
Box.test(arima_model$residuals, lag=20, type = "Ljung-Box")
acf(arima_model$residuals, lag.max = 24, main="ACF of the model")

Box.test(arima_model$residuals, lag=20, type = "Ljung-Box")
#library(tseries)
jarque.bera.test(arima_model$residuals)

arima_model.forecast = forecast(arima_model, h=60)
arima_model.forecast
x = array(as.numeric(arima_model.forecast$mean), dim=60)
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
plot(arima_model.forecast, xlab = "Years", ylab = "SPI")

library(TSPred)
plotarimapred(data.test, arima_model.forecast, xlim = c(2016,2020), range.percent=0.05)
accuracy(arima_model.forecast, data.test)


