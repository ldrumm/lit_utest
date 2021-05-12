"""lit_utest - llvm-lit module for first-class utest.h unit test support"""

__version__ = '0.1.0'
__author__ = 'ldrumm <ldrumm@rtps.co>'
__all__ = []

import os
import subprocess

import lit
from lit.util import to_string as tostr

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError


class UTestRunner(lit.formats.ShTest):
    def parsers(self):
        script = []
        return (
            lit.TestRunner.IntegratedTestKeywordParser(
                'UTEST:',
                lit.TestRunner.ParserKind.COMMAND,
                initial_value=script
            ),
            script
        )

    def run(self, test, t, name, cfg, tmp, cwd):
        out, err, code, timeout = lit.TestRunner.executeScriptInternal(
            test, cfg, tmp, [' '.join([t, '--filter=%s' % name])], cwd
        )
        if timeout:
            status = lit.Test.TIMEOUT
        else:
            status = lit.Test.PASS if not code else lit.Test.FAIL

        return lit.Test.Result(status, 'stdout:\n%s\nstderr:\n%s' % (out, err))

    def run_foreach(self, test, bin, cfg, tmp, cwd):
        try:
            tests = map(
                str.strip,
                tostr(subprocess.check_output([bin, '--list-tests']))
                .splitlines()
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            return lit.Test.Result(lit.Test.FAIL)

        results = {
            name: self.run(test, bin, name, cfg, tmp, cwd)
            for name in tests
        }
        ok = all(map(lambda r: not r.code.isFailure, results.values()))
        output = ('-' * 80).join(r.output for r in results.values())
        main = lit.Test.Result(lit.Test.PASS if ok else lit.Test.FAIL, output)
        for name, result in results.items():
            main.addMicroResult('%s[%s] -> %s' % (
                test.getFullName(), name, result.code.name),
                result
            )

        return main

    def execute(self, test, cfg):
        parsers, results = zip(self.parsers())
        # `results` is set by reference by `parseIntegratedTestScript`
        script = lit.TestRunner.parseIntegratedTestScript(
            test,
            additional_parsers=parsers,
            require_script=False
        )
        if isinstance(script, lit.Test.Result):
            # unsupported
            return script
        tmp_dir, tmp_base = lit.TestRunner.getTempPaths(test)
        execdir = os.path.dirname(test.getExecPath())
        substs = lit.TestRunner.getDefaultSubstitutions(
            test,
            tmp_dir,
            tmp_base,
            False
        )
        name = os.path.split(test.getSourcePath())[1] + '.tmp'
        out_bin = os.path.join(execdir, name)
        substs.insert(0, ('%utest_bin', out_bin))
        s = lit.TestRunner.applySubstitutions(results[0], substs)
        if not s:
            return lit.Test.Result(lit.Test.UNRESOLVED)
        lit.util.mkdir_p(execdir)
        out, err, code, timeout = lit.TestRunner.executeScriptInternal(
                test, cfg, tmp_base, s, execdir)
        if code or timeout:
            return lit.Test.Result(
                lit.Test.FAIL, 'Failed to build utest binary:\n' + err + out)

        return self.run_foreach(test, out_bin, cfg, tmp_base, execdir)
