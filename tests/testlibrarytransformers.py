import unittest

from composerstoolkit.core import CTEvent, CTSequence, chain
from composerstoolkit.builder.transformers import transpose, invert

class CTLibraryTransformerTests(unittest.TestCase):
    
    def test_transpose(self):
        src = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ])
        
        transposed = src |chain| transpose(1)
        assert transposed.events == [
            CTEvent(61,100),
            CTEvent(63,100),
            CTEvent(65,100),
            CTEvent(61,100),
        ]
        
    def test_transpose_down(self):
        src = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ])
        
        transposed = src |chain| transpose(-1)
        assert transposed.events == [
            CTEvent(59,100),
            CTEvent(61,100),
            CTEvent(63,100),
            CTEvent(59,100),
        ]
        
    def test_invert(self):
        src = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ])
        
        inverted = src |chain| invert()
        assert inverted.events == [
            CTEvent(60,100),
            CTEvent(58,100),
            CTEvent(56,100),
            CTEvent(60,100),
        ]
        
    def test_invert_specified_axis(self):
        src = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ])
        
        inverted = src |chain| invert(62)
        assert inverted.events == [
            CTEvent(64,100),
            CTEvent(62,100),
            CTEvent(60,100),
            CTEvent(64,100),
        ]
        
    def test_invert_specified_axis_lower(self):
        src = CTSequence([
            CTEvent(60,100),
            CTEvent(62,100),
            CTEvent(64,100),
            CTEvent(60,100),
        ])
        
        inverted = src |chain| invert(59)
        assert inverted.events == [
            CTEvent(58,100),
            CTEvent(56,100),
            CTEvent(54,100),
            CTEvent(58,100),
        ]