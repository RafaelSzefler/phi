# -*- coding: utf-8 -*-
from io import BytesIO

import pytest

from phi.request.multipart.boundary_reader import BoundaryReader, dry_generator

from tests.dependencies import mock


CONTENT = (
    "preamble: a b c d e f g h i j k l m n o q p r s test"
    "\r\n--foo\r\n"
    "Type: test\r\n"
    "Header: xyz\r\n"
    "\r\n"
    "first attachment"
    "\r\n--foo\r\n"
    "\r\n"
    "second attachment"
    "\r\n--foo--\r\n"
    "epilogue"
)


@pytest.fixture
def br():
    stream = BytesIO(CONTENT)
    length = len(CONTENT)
    reader = BoundaryReader(
        stream, "foo", length
    )
    reader.MIN_BUFFER_SIZE = 12
    return reader


class TestBoundaryReader(object):
    @pytest.mark.parametrize("buffer_size, result", [
        (
            15, [
                ["preamble: a b c", " d e f g h i j ", "k l m n o q p r", " s test"],
                ["Type: test\r\nHe", "ader: xyz\r\n\r\nfi", "rst attachment"],
                ["\r\nsecon", "d attachment"]
            ]
        ),
        (
            25, [
                ["preamble: a b c d e f g h", " i j k l m n o q p r s test"],
                ["Type: test\r\nHe", "ader: xyz\r\n\r\nfirst attachment"],
                ["\r\nsecond attachment"]
            ]
        ),
        (
            50, [
                ["preamble: a b c d e f g h i j k l m n o q p r s test"],
                ["Type: test\r\nHeader: xyz\r\n\r\nfirst attachment"],
                ["\r\nsecond attachment"]
            ]
        )
    ])
    def test_read_until_next_boundary(self, buffer_size, result, br):
        br.initialize(buffer_size)
        data = []
        counter = 0
        while not br.is_dry():
            counter += 1
            data.append(
                list(
                    br.read_until_next_boundary(buffer_size)
                )
            )
            if counter >= 100:
                raise Exception(
                    "Too many iterations! read_until_next_boundary is broken!"
                )

        assert data == result

    def test_read_until_next_boundary_exc(self, br):
        br.MIN_BUFFER_SIZE = 100
        with pytest.raises(ValueError):
            list(br.read_until_next_boundary(99))

    def test_initialize(self, br):
        br.initialize()
        assert br._leftover == b"preamble: a "

    def test_read_until_next_boundary_dry(self, br):
        br._is_dry = True
        data = list(br.read_until_next_boundary(100))
        assert data == [b""]

    def test_is_dry(self, br):
        dry = mock.Mock()
        br._is_dry = dry
        assert br.is_dry() is dry

    @pytest.mark.parametrize("read, size", [
        (1, 5), (10, 10), (15, 10)
    ])
    def test_fully_read(self, br, read, size):
        br._read = read
        br._size = size
        assert br.fully_read() is (read == size)

    def test__read_chunk(self, br):
        data = []
        for _ in xrange(10):
            data.append(br._read_chunk(45))
        assert data == [
            'preamble: a b c d e f g h i j k l m n o q p r',
            ' s test\r\n--foo\r\nType: test\r\nHeader: xyz\r\n\r\nfi',
            'rst attachment\r\n--foo\r\n\r\nsecond attachment\r\n-',
            '-foo--\r\nepilogue',
            '', '', '', '', '', ''
        ]


def test_dry_generator():
    side_effects = []

    def gen():
        yield 1
        side_effects.append(2)
        yield 3
        side_effects.append(4)
        yield 5
        side_effects.append(6)

    dry_generator(gen())
    assert side_effects == [2, 4, 6]
