<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>AWPythonParts\TestSlab.py</Name>
        <Title>Balkon-Test</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>BalkonPP</Text>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Gabaryt</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>Width</Name>
                <Text>Szerokość</Text>
                <Value>5000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Length</Name>
                <Text>Wysięg</Text>
                <Value>2000.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>Thickness</Name>
                <Text>Grubość</Text>
                <Value>250.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Waterstop</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>ws_height</Name>
                <Text>Wysokość Waterstopa</Text>
                <Value>50.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>ws_length</Name>
                <Text>Długość Waterstopa</Text>
                <Value>150.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>ws_angle</Name>
                <Text>Kąt spadku waterstopa (stopnie)</Text>
                <Value>45</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Spadek</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>sl_height</Name>
                <Text>Wysokość spadku</Text>
                <Value>50</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander1</Name>
            <Text>Kapinos</Text>
            <Value>False</Value>
            <ValueType>Expander</ValueType>
            <Parameter>
                <Name>is_front</Name>
                <Text>Kapinos na wolnej krawędzi</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>is_side</Name>
                <Text>Kapinos po bokach</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>drip_start</Name>
                <Text>Odległość od krawędzi zamocowania</Text>
                <Value>300</Value>
                <Visible>is_side==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>drip_height</Name>
                <Text>Wysokość kapinosa</Text>
                <Value>10.</Value>
                <Visible>is_side==True or is_front==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>drip_width</Name>
                <Text>Szerokość kapinosa</Text>
                <Value>15.</Value>
                <Visible>is_side==True or is_front==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>drip_offset</Name>
                <Text>Odległość osi kapinosa do kraw. balkonu</Text>
                <Value>50</Value>
                <Visible>is_side==True or is_front==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>
    </Page>

</Element>
