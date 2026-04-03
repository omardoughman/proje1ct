class Omar < Formula
  include Language::Python::Virtualenv

  desc "Omar package manager"
  homepage "https://github.com/yourname/omar"
  url "https://github.com/yourname/omar/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "PUT_SHA256_HERE"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end
end
