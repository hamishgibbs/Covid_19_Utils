
data <- read_csv('/Users/hamishgibbs/Documents/Covid-19/Other_Projects/citymapper/output/citymapper_data.csv')

require(ggplot2)

p <- data %>% 
  mutate(country = substr(region_id, 1, 2)) %>% 
  ggplot() +
  theme_bw() +
  geom_path(aes(x = date, y = value, group = region_id, colour = country), size = 0.2) +
  theme(legend.position = c(0.9, 0.8),
        legend.background = element_rect(fill = 'transparent'),
        legend.text = element_text(size = 6),
        legend.key.size = unit(0.1, "cm"),
        text = element_text(size = 7))

ggsave('~/Downloads/citymapper.png', p, 
       width = 4, 
       height = 4, 
       units = 'in')
