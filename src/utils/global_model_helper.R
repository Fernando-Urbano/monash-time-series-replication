#' Create Input Matrix for Global Models Training
#'
#' This function prepares the embedded matrix and final lags for training global models based on a given lag. 
#' It performs mean normalization on each time series in the dataset, embeds the series with the specified lag, 
#' and prepares the final lags for model training. The process includes normalizing time series by their mean 
#' (replacing mean of 0 with 1 to avoid division by zero), embedding the time series with a given lag, and 
#' preparing final lags for the training set.
#'
#' param dataset A list of numeric vectors, where each vector represents a time series.
#' param lag An integer specifying the number of lags to use for embedding.
#'
#' return A list containing three elements: 
#'         - `embedded_series`: a dataframe where each row is an embedded time series with columns for the target variable 'y' 
#'           and its lags.
#'         - `final_lags`: a dataframe of the final lag values for each time series, to be used as part of the test set.
#'         - `series_means`: a vector of means for each time series used for normalization.
#'
#' examples
#' data <- list(c(1,2,3,4,5), c(2,3,4,5,6))
#' result <- create_input_matrix(data, 2)
#' result$embedded_series
#' result$final_lags
#' result$series_means
# Creating embedded matrix and final lags to train the global models for a given lag
create_input_matrix <- function(dataset, lag){
  embedded_series <- NULL
  final_lags <- NULL
  series_means <- NULL
  
  for (i in 1:length(dataset)) {
    print(i)
    time_series <- as.numeric(dataset[[i]])
    
    mean <- mean(time_series)
    
    # Mean normalisation
    if(mean == 0)
      mean <- 1 # Avoid division by zero
    
    time_series <- time_series / mean
    series_means <- c(series_means, mean)
    
    # Embed the series
    embedded <- embed(time_series, lag + 1)
    
    if (!is.null(embedded_series)) {
      embedded_series <- as.matrix(embedded_series)
    }
    embedded_series <- rbind(embedded_series, embedded)
    
    # Creating the test set
    if (!is.null(final_lags)) {
      final_lags <- as.matrix(final_lags)
    }
    
    current_series_final_lags <- t(as.matrix(rev(tail(time_series, lag))))
    
    final_lags <- rbind(final_lags, current_series_final_lags)
  }
  
  # Adding proper column names for embedded_series and final_lags
  embedded_series <- as.data.frame(embedded_series)
  colnames(embedded_series)[1] <- "y"
  colnames(embedded_series)[2:(lag + 1)] <- paste("Lag", 1:lag, sep = "")
  
  final_lags <- as.data.frame(final_lags)
  colnames(final_lags)[1:lag] <- paste("Lag", 1:lag, sep = "")
  
  list(embedded_series, final_lags, series_means)
}
