library(rbenchmark)

x <- 10240
factors <- c()

# benchmark(
#     "Loop" = {
#         loop_factors <- c(1)
#         for (i in 2:x) {
#             if (x %% i == 0) {
#                 loop_factors <- c(loop_factors, i)
#             }
#         }
#     }
# )
arr = array(0, c(0,0))

benchmark(
    # "Loop" = {
    #     loop_factors <- c(1)
    #     for (i in 2:x) {
    #         if (x %% i == 0) {
    #             loop_factors <- c(loop_factors, i)
    #         }
    #     }
        
    # },
    # "Vector" = {
    #     loop_factors <- (1:x)[(x %% 1:x) == 0]
        
    # },
    # "Vector Readable" = {
    #     remainders <- x %% 1:x
    #     true_false <- remainders == 0
    #     loop_factors <- (1:x)[true_false]
    #     print(loop_factors)
    # }
    "seq_along" = {
        for(i in 0:1000) {
            length(arr)
        }

    },
        "seq_along" = {
        for(i in 0:1000) {
              seq_along(arr)
        }

    }
    
)
