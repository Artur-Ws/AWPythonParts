<?xml version="1.0" encoding="utf-8"?>
<Element>
    <Script>
        <Name>AWPythonParts\TestSlab.py</Name>
        <Title>Balkon-Test</Title>
        <Version>1.0</Version>
    </Script>

    <Page>
        <Name>Page1</Name>
        <Text>Geometria</Text>

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
                <Text>Grubość (koniec wysięgu)</Text>
                <Value>250.</Value>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>sl_height</Name>
                <Text>Wysokość spadku</Text>
                <Value>50</Value>
                <ValueType>Length</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander2</Name>
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
            <Name>Expander4</Name>
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

    <Page>
        <Name>ReinfTab</Name>
        <Text>Zbrojenie</Text>
        <Parameter>
            <Name>Expander5</Name>
            <Text>Siatka dolna</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>bottom_checkbox</Name>
                <Text>Twórz siatkę dolną</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>bottom_SteelGrade</Name>
                <Text>Typ zbrojenia</Text>
                <Value>4</Value>
                <Visible>bottom_checkbox==True</Visible>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>bottom_down_ConcreteCover</Name>
                <Text>Otulina dolna</Text>
                <Value>30</Value>
                <Visible>bottom_checkbox==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>bottom_side_ConcreteCover</Name>
                <Text>Otulina boczna</Text>
                <Value>100</Value>
                <Visible>bottom_checkbox==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>bottom_first_diameter</Name>
                <Text>Średnica prętów głównych</Text>
                <Value>6</Value>
                <Visible>bottom_checkbox==True</Visible>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>bottom_first_spacing</Name>
                <Text>Rozzstaw prętów głównych</Text>
                <Value>150</Value>
                <ValueList>50|75|100|125|150|175|200|225|250|275|300</ValueList>
                <Visible>bottom_checkbox==True</Visible>
                <ValueType>LengthComboBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>bottom_second_diameter</Name>
                <Text>Średnica prętów poprzecznych</Text>
                <Value>6</Value>
                <Visible>bottom_checkbox==True</Visible>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>bottom_second_spacing</Name>
                <Text>Rozzstaw prętów poprzecznych</Text>
                <Value>150</Value>
                <Visible>bottom_checkbox==True</Visible>
                <ValueType>double</ValueType>
            </Parameter>

        </Parameter>
        <Parameter>
            <Name>Expander6</Name>
            <Text>Siatka górna</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>top_checkbox</Name>
                <Text>Twórz siatkę górną</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>up_SteelGrade</Name>
                <Text>Typ zbrojenia</Text>
                <Value>4</Value>
                <Visible>top_checkbox==True</Visible>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>
            <Parameter>
                <Name>up_ConcreteCover</Name>
                <Text>Otulina</Text>
                <Value>30</Value>
                <Visible>top_checkbox==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>up_first_diameter</Name>
                <Text>Średnica prętów głównych</Text>
                <Value>12</Value>
                <Visible>top_checkbox==True</Visible>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>up_first_spacing</Name>
                <Text>Rozzstaw prętów głównych</Text>
                <Value>150</Value>
                <Visible>top_checkbox==True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>up_second_diameter</Name>
                <Text>Średnica prętów poprzecznych</Text>
                <Value>6</Value>
                <Visible>top_checkbox==True</Visible>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>up_second_spacing</Name>
                <Text>Rozzstaw prętów poprzecznych</Text>
                <Value>150</Value>
                <ValueList>50|75|100|125|150|175|200|225|250|275|300</ValueList>
                <Visible>top_checkbox==True</Visible>
                <ValueType>LengthComboBox</ValueType>
            </Parameter>

        </Parameter>


        <Parameter>
            <Name>Expander7</Name>
            <Text>Ubary po bokach</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>side_ubars_checkbox</Name>
                <Text>Twórz ubary po bokach</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>side_ubars_SteelGrade</Name>
                <Text>Typ zbrojenia</Text>
                <Value>4</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>ReinfSteelGrade</ValueType>
            </Parameter>

            <Parameter>
                <Name>side_ubars_side_cover</Name>
                <Text>Otulina od boku</Text>
                <Value>30</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_top_cover</Name>
                <Text>Otulina od góry</Text>
                <Value>40</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_bottom_cover</Name>
                <Text>Otulina od dołu</Text>
                <Value>30</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>side_ubars_diameter</Name>
                <Text>Średnica Ubarów</Text>
                <Value>6</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_spacing</Name>
                <Text>Rozstaw Ubarów</Text>
                <Value>150</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_ends_length</Name>
                <Text>Długość ramion</Text>
                <Value>300</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>double</ValueType>
            </Parameter>

            <Parameter>
                <Name>side_ubars_hook_checkbox</Name>
                <Text>Haki na końcach</Text>
                <Value>False</Value>
                <Visible>side_ubars_checkbox==True</Visible>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_start_hook</Name>
                <Text>Długość górnego haka</Text>
                <Value>0</Value>
                <Visible>side_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_start_hook_angle</Name>
                <Text>Kąt gięcia górnego haka</Text>
                <Value>90</Value>
                <Visible>side_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_end_hook</Name>
                <Text>Długość dolnego haka</Text>
                <Value>0</Value>
                <Visible>side_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>side_ubars_end_hook_angle</Name>
                <Text>Kąt gięcia dolnego haka</Text>
                <Value>90</Value>
                <Visible>side_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander8</Name>
            <Text>Ubary na wolnej krawędzi</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>front_ubars_checkbox</Name>
                <Text>Twórz ubary na wolnej krawędzi</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>front_ubars_side_cover</Name>
                <Text>Otulina od boku</Text>
                <Value>30</Value>
                <Visible>front_ubars_checkbox == True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_top_cover</Name>
                <Text>Otulina od góry</Text>
                <Value>30</Value>
                <Visible>front_ubars_checkbox == True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_bottom_cover</Name>
                <Text>Otulina od dołu</Text>
                <Value>40</Value>
                <Visible>front_ubars_checkbox == True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>front_ubars_diameter</Name>
                <Text>Średnica Ubarów</Text>
                <Value>6</Value>
                <Visible>front_ubars_checkbox == True</Visible>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_spacing</Name>
                <Text>Rozstaw Ubarów</Text>
                <Value>150</Value>
                <Visible>front_ubars_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_ends_length</Name>
                <Text>Długość ramion</Text>
                <Value>300</Value>
                <Visible>front_ubars_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>

            <Parameter>
                <Name>front_ubars_hook_checkbox</Name>
                <Text>Haki na końcach</Text>
                <Value>False</Value>
                <Visible>front_ubars_checkbox == True</Visible>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_start_hook</Name>
                <Text>Długość górnego haka</Text>
                <Value>0</Value>
                <Visible>front_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_start_hook_angle</Name>
                <Text>Kąt gięcia górnego haka</Text>
                <Value>90</Value>
                <Visible>front_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_end_hook</Name>
                <Text>Długość dolnego haka</Text>
                <Value>0</Value>
                <Visible>front_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>front_ubars_end_hook_angle</Name>
                <Text>Kąt gięcia dolnego haka</Text>
                <Value>90</Value>
                <Visible>front_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
        </Parameter>

        <Parameter>
            <Name>Expander9</Name>
            <Text>Ubary na krawędzi zamocowania</Text>
            <ValueType>Expander</ValueType>

            <Parameter>
                <Name>back_ubars_checkbox</Name>
                <Text>Twórz ubary na krawędzi zamocowania</Text>
                <Value>True</Value>
                <ValueType>CheckBox</ValueType>
            </Parameter>

            <Parameter>
                <Name>back_ubars_side_cover</Name>
                <Text>Otulina od boku</Text>
                <Value>30</Value>
                <Visible>back_ubars_checkbox == True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_top_cover</Name>
                <Text>Otulina od góry</Text>
                <Value>40</Value>
                <Visible>back_ubars_checkbox == True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_bottom_cover</Name>
                <Text>Otulina od dołu</Text>
                <Value>30</Value>
                <Visible>back_ubars_checkbox == True</Visible>
                <ValueType>Length</ValueType>
            </Parameter>

            <Parameter>
                <Name>back_ubars_diameter</Name>
                <Text>Średnica Ubarów</Text>
                <Value>6</Value>
                <Visible>back_ubars_checkbox == True</Visible>
                <ValueType>ReinfBarDiameter</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_spacing</Name>
                <Text>Rozstaw Ubarów</Text>
                <Value>150</Value>
                <Visible>back_ubars_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_ends_length</Name>
                <Text>Długość ramion</Text>
                <Value>300</Value>
                <Visible>back_ubars_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>

            <Parameter>
                <Name>back_ubars_hook_checkbox</Name>
                <Text>Haki na końcach</Text>
                <Value>False</Value>
                <Visible>back_ubars_checkbox == True</Visible>
                <ValueType>CheckBox</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_start_hook</Name>
                <Text>Długość górnego haka</Text>
                <Value>0</Value>
                <Visible>back_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_start_hook_angle</Name>
                <Text>Kąt gięcia górnego haka</Text>
                <Value>90</Value>
                <Visible>back_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_end_hook</Name>
                <Text>Długość dolnego haka</Text>
                <Value>0</Value>
                <Visible>back_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
            <Parameter>
                <Name>back_ubars_end_hook_angle</Name>
                <Text>Kąt gięcia dolnego haka</Text>
                <Value>90</Value>
                <Visible>back_ubars_hook_checkbox == True</Visible>
                <ValueType>double</ValueType>
            </Parameter>
        </Parameter>
    </Page>
</Element>
