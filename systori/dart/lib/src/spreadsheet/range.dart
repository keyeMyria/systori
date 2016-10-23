import 'package:quiver/collection.dart';
import 'package:systori/decimal.dart';
import 'cell.dart';


class RangeResult {

    int group;
    int start;
    int end;
    Decimal value;

    bool isHit(int idx) => start <= idx && idx <= end;
    bool get isEmpty => start == -1;

    RangeResult() {
        reset();
    }

    reset() {
        start = -1;
        end = -1;
        value = new Decimal();
    }
}


class RangeCache extends DelegatingMap<String,RangeResult> {
    final Map<String,RangeResult> _cache = {};
    Map<String,RangeResult> get delegate => _cache;

    reset() {
        // there could be ranges still holding references to results
        // so we want to reset those first
        _cache.values.forEach((r)=>r.reset());
        // now clear out the cache
        _cache.clear();
    }

}


class RangeList extends DelegatingList<Range> {

    final List<Range> _ranges = [];
    List<Range> get delegate => _ranges;

    RangeList(String eq, RangeCache cache) {
        cache.values.forEach((r)=>r.group=null);
        int nextGroup = 1;
        for (var m in Range.PATTERN.allMatches(eq.toUpperCase())) {
            var src = m.group(0);
            var result = cache.putIfAbsent(src, ()=>new RangeResult());
            if (result.group == null)
                result.group = nextGroup++;
            _ranges.add(new Range(result,
                    m.group(1), m.group(2),
                    m.group(3), m.group(4), // startEquation, start
                    m.group(5), m.group(6), m.group(7), // exclusive range
                    m.group(8), m.group(9), // endEquation, end
                    m.start, m.end, src
            ));
        }
    }

    calculate(List<Cell> getColumn(int columnIdx), RangeCache cache, int thisColumn) {
        for (var range in _ranges) {
            var columnIdx = range.column != null ? range.column : thisColumn;
            cache.putIfAbsent(range.src, ()=>range.result);
            if (range.result.isEmpty)
                range.calculate(getColumn(columnIdx));
        }
    }

    String resolve(String equation) {
        var buffer = new StringBuffer();
        int lastEnd = 0;
        for (var range in _ranges) {
            buffer.write(equation.substring(lastEnd, range.srcStart));
            buffer.write(range.result.value.number);
            lastEnd = range.srcEnd;
        }
        buffer.write(equation.substring(lastEnd));
        return buffer.toString();
    }


}


class Range {

    static final RegExp PATTERN = new RegExp(r'([ABC]?)([!@])(&?)(\d*)(\[?)(:?)(\]?)(&?)(\d*)');

    final int column;
    final String direction;
    final bool range;

    final int start;
    final bool isStartEquation;
    final bool isStartExclusive;

    final int end;
    final bool isEndExclusive;
    final bool isEndEquation;
    bool get isEndOpen => end == null && !isEndEquation;

    final RangeResult result;
    final int srcStart;
    final int srcEnd;
    final String src;

    Range(this.result, String column, this.direction,
        startEquation, start,
        exclusiveStart, range, exclusiveEnd,
        endEquation, end,
        this.srcStart, this.srcEnd, this.src):
            column = column.isNotEmpty ? 'ABC'.indexOf(column) : null,
            isStartEquation = startEquation=='&',
            start = int.parse(start, onError: (source) => 1),
            isStartExclusive = exclusiveStart=='[',
            range = exclusiveStart=='[' || exclusiveEnd==']' || range==':',
            isEndExclusive = exclusiveEnd==']',
            isEndEquation = endEquation=='&',
            end = int.parse(end, onError: (source) => endEquation=='&' ? 1 : null)
    ;

    Decimal calculate(List<Cell> _cells) {

        result.reset();

        if ((end != null && !isEndEquation && start > end) ||
            (isStartEquation && start > 1 && isEndEquation && isEndOpen)) // prevent: !&2:&
            return result.value;

        Iterator<Cell> cells = _cells.iterator;
        if (direction == '!') {
            cells = _cells.reversed.iterator;
        }

        int i = 0;
        bool inside = false;
        int equationIdx = 0;
        int lastIdx = _cells.length;
        while (cells.moveNext()) { i++;

        if (cells.current.hasEquation) equationIdx++;

        if ((!isStartEquation && start == i) ||
            (isStartEquation && cells.current.hasEquation && start == equationIdx)) {
            inside = true;
            if (isStartExclusive)
                // if we're at the start and [ then don't add this row
                continue;
        }

        if (!inside)
            continue; // keep searching for the start of range

        if (result.start == -1 && result.end == -1) {
            if (direction == '!')
                result.end = lastIdx-i;
            else
                result.start = i-1;
        }

        if ((!isEndEquation && end == i) ||
            (isEndEquation && cells.current.hasEquation && end == equationIdx) ||
            lastIdx == i) {
            // last row means we're not inside anymore
            inside = false;
            if (isEndExclusive)
                // if we're at the end and ] then don't add this row, break immediately
                break;
            if (lastIdx == i && isEndEquation && (!cells.current.hasEquation || end != equationIdx)) {
                // we've made it to the end without finding any equations
                // this whole range is a dud, clear everything and exit
                result.reset();
                break;
            }
        }

        result.value += cells.current.value;

        if (direction == '!')
            result.start = lastIdx-i;
        else
            result.end = i-1;

        if (!inside || !range)
            break;

        }

        return result.value;
    }

}

