#!/usr/bin/python3

from lxml import html


def example1():
    print("Example 1")

    html_str = """
<html>
<body>
  <h1>SCRAPE ME</h1>
</body>
</html>
    """

    tree = html.fromstring(html_str)

    h1 = tree.xpath("/html/body/h1")
    print(h1)
    print(h1[0].text)

    h1 = tree.xpath("//h1")
    print(h1)
    print(h1[0].text)
    
    root = tree.xpath('/html')[0]
    body = root.xpath('./body')[0]
    h1 = body.xpath('./h1')
    print(h1)
    print(h1[0].text)


def example2():
    print("Example 2")

    html_str = """
<html>
<body>
  <div id="main">SCRAPE ME</div>
  <div id="secondary">...</div>
</body>
</html>
    """

    tree = html.fromstring(html_str)

    main_div = tree.xpath('//div[@id="main"]')
    print(main_div)
    print(main_div[0].text)

    main_div = tree.xpath('//*[@id="main" and not(@id="secondary")]')
    print(main_div)
    print(main_div[0].text)


def example3():
    print("Example 3")

    html_str = """
<html>
  <body>
    <a href="https://lxml.de" label="SCRAPE ME">lxml</a>
  </body>
</html>
    """

    tree = html.fromstring(html_str)

    label = tree.xpath("//a/@label")
    print(label)


def example4():
    print("Example 4")

    html_str = """
<html>
  <body>
    <div>ignore</div>
    <div class="a b">ignore</div>
    <div class="a b c">SCRAPE ME</div>
  </body>
</html>
    """

    tree = html.fromstring(html_str)

    text = tree.xpath('//div[contains(@class, "c")]/text()')
    print(text)

    text = tree.xpath('//div[contains(text(), "ME")]/text()')
    print(text)


def example5():
    print("Example 5")

    html_str = """
<html>
  <body>
    <div>ignore</div>
    <div>SCRAPE ME<strong>!</strong></div>
  </body>
</html>
    """

    tree = html.fromstring(html_str)

    d = tree.xpath('//div[./strong[text()="!"]]')
    print(d)
    print(d[0].text_content())


def example6():
    print("Example 6")

    html_str = """
<html>
  <body>
    <table>
      <tr>
        <th>Data 1</th>
        <th>Data 2</th>
      </tr>
      <tr>
        <td>ignore</td>
        <td>...</td>
      </tr>
      <tr>
        <td>scrape</td>
        <td>SCRAPE ME</td>
      </tr>
    </table>
  </body>
</html>
    """

    tree = html.fromstring(html_str)

    td = tree.xpath('//tr[./td[text()="scrape"]]/td[2]')
    print(td)
    print(td[0].text)


def main():
    example1()
    example2()
    example3()
    example4()
    example5()
    example6()


if __name__ == "__main__":
    main()
