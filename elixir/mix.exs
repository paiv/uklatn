defmodule Paiv.UkrainianLatin.MixProject do
  use Mix.Project

  def project do
    [
      app: :uklatn,
      version: "1.17.0",
      elixir: "~> 1.12",
      name: "Paiv.UkrainianLatin",
      description: "Ukrainian Cyrillic transliteration to Latin script",
      homepage_url: "https://github.com/paiv/uklatn",
      package: %{
        licenses: ["MIT"],
        links: %{
          "GitHub" => "https://github.com/paiv/uklatn",
          "Sponsor" => "https://www.paypal.com/donate/?hosted_button_id=4BQ2Y97YUMM7L"
        }
      }
    ]
  end

  def application do
    []
  end
end
