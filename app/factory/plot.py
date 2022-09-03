from typing import Any, Dict
import matplotlib.pyplot as plt
from wordcloud import WordCloud


class Plotter:
    wc_base_params: Dict = dict(
        background_color="white",
        max_words=2000,
        contour_width=3,
        contour_color="steelblue"
    )

    def set_wcloud(self):
        self.wc = WordCloud(**dict(
            **self.wc_base_params,
            stopwords=set(self._stopwords),
            # mask=self.image_mask,
        ))

    def generate_cloud(self):
        self.wc.generate(self._text)

    def plot_cloud(self, destination):
        plt.figure()
        plt.imshow(self.wc, interpolation="bilinear")
        # plt.figure()
        # plt.imshow(self.image_mask, cmap=plt.cm.gray, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(destination)

    def plot_cloud_to_buffer(self, buffer: Any):
        self.plot_cloud(buffer)
