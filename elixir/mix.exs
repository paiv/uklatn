defmodule Paiv.UkrainianLatin.MixProject do
  use Mix.Project

  def project do
    [
      app: :uklatn,
      version: "1.17.0",
      elixir: "~> 1.12",
      description: "Ukrainian Cyrillic transliteration to Latin script",
      homepage_url: "https://github.com/paiv/uklatn",
      package: %{
        licenses: ["MIT"],
        links: %{
          "GitHub" => "https://github.com/paiv/uklatn",
          "Sponsor" => "https://www.paypal.com/donate/?hosted_button_id=4BQ2Y97YUMM7L"
        }
      },
      deps: deps()
    ]
  end

  def application do
    []
  end

  defp deps do
    [
      {:ex_doc, ">= 0.0.0", only: :dev, runtime: false}
    ]
  end
end
