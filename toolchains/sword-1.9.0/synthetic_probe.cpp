// SPDX-License-Identifier: MIT
// Original JEB diagnostic source. A binary linked with libsword is subject to GPL-2.0.
// This probe accepts only the isolated JEBSynthetic fixture, never a historical module.
#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <swmgr.h>
#include <swmodule.h>
#include <versekey.h>
#include <ztext.h>
#include <zipcomprs.h>

class StoredProbe : public sword::zText {
public:
    StoredProbe(const char *path) : sword::zText(path, "JEBSynthetic", "Synthetic only",
        BOOKBLOCKS, new sword::ZipCompress(), 0, sword::ENC_UTF8, sword::DIRECTION_LTR,
        sword::FMT_OSIS, "sr-Latn", "Calvin") {}
    std::string stored(const sword::VerseKey &key) const {
        long start = 0;
        unsigned short size = 0;
        unsigned long block = 0;
        findOffset(key.getTestament(), key.getTestamentIndex(), &start, &size, &block);
        sword::SWBuf buffer;
        zReadText(key.getTestament(), start, size, block, buffer);
        return std::string(buffer.c_str(), buffer.size());
    }
};

static void quoted(const std::string &s) {
    std::cout << '"';
    const char *hex = "0123456789abcdef";
    for (unsigned char c : s) {
        if (c == '"' || c == '\\') std::cout << '\\' << c;
        else if (c < 32) std::cout << "\\u00" << hex[c >> 4] << hex[c & 15];
        else std::cout << c;
    }
    std::cout << '"';
}

static std::string slot(const sword::VerseKey *key) {
    return std::string(key->getOSISBookName()) + "." + std::to_string(key->getChapter()) +
           "." + std::to_string(key->getVerse());
}

int main(int argc, char **argv) {
    if (argc < 3 || argc > 35) return 2;
    sword::SWMgr mgr(argv[1], true, 0, false, false);
    if (mgr.getModules().size() != 1) return 3;
    sword::SWModule *mod = mgr.getModule("JEBSynthetic");
    if (!mod) return 4;
    if (std::string(mod->getConfigEntry("DataPath")) != "./modules/texts/ztext/jebsynthetic/" ||
        std::string(mod->getConfigEntry("Versification")) != "Calvin" ||
        std::string(mod->getConfigEntry("ModDrv")) != "zText") return 8;
    std::string dataPath = std::string(argv[1]) + "/modules/texts/ztext/jebsynthetic/";
    StoredProbe stored(dataPath.c_str());
    std::vector<std::unique_ptr<sword::VerseKey>> previous;
    std::vector<bool> present;
    for (int i = 2; i < argc; ++i) {
        std::unique_ptr<sword::SWKey> generic(mod->createKey());
        auto *key = dynamic_cast<sword::VerseKey *>(generic.get());
        if (!key) return 5;
        key->setIntros(true);
        key->setAutoNormalize(false);
        key->setText(argv[i]);
        if (key->popError()) return 6;
        std::string id = slot(key);
        bool allowed = false;
        for (const char *book : {"Gen.", "Matt.", "Mark.", "Luke.", "John."}) {
            if (id.find(book) == 0) allowed = true;
        }
        if (!allowed) return 7;
        bool exists = mod->hasEntry(key);
        std::string link;
        if (exists) {
            for (size_t j = 0; j < previous.size(); ++j) {
                if (present[j] && mod->isLinked(key, previous[j].get())) {
                    link = slot(previous[j].get());
                    break;
                }
            }
        }
        mod->setKey(*key);
        std::string raw = exists ? mod->getRawEntry() : "";
        std::string storedRaw = exists ? stored.stored(*key) : "";
        std::cout << "{\"schema_version\":\"1.0\",\"module_id\":\"JEBSynthetic\",\"scheme\":";
        quoted(mod->getConfigEntry("Versification"));
        std::cout << ",\"source_type\":"; quoted(mod->getConfigEntry("SourceType"));
        std::cout << ",\"osis_id\":"; quoted(id);
        std::cout << ",\"entry_kind\":";
        quoted(key->getChapter() == 0 ? "book_introduction" :
               key->getVerse() == 0 ? "chapter_introduction" : "verse");
        std::cout << ",\"has_entry\":" << (exists ? "true" : "false") << ",\"linked_to\":";
        if (link.empty()) std::cout << "null"; else quoted(link);
        std::cout << ",\"link_scope\":\"requested_keys_only\",\"raw_length_bytes\":" << raw.size();
        std::cout << ",\"engine_osis\":"; quoted(raw);
        std::cout << ",\"stored_length_bytes\":" << storedRaw.size();
        std::cout << ",\"stored_osis\":"; quoted(storedRaw); std::cout << "}\n";
        previous.emplace_back(new sword::VerseKey(*key));
        present.push_back(exists);
    }
    return 0;
}
